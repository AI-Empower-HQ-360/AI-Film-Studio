"""Worker task executor for autonomous task processing"""
import time
from typing import Optional, Dict, Any
from datetime import datetime
from src.models.workflow import TaskMessage, TaskType, TaskStatus
from src.services.queue import get_task_queue
from src.services.storage import get_job_store
from src.services.orchestrator import get_orchestrator
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class ModelExecutor:
    """Mock model execution - replace with actual AI model calls"""
    
    def generate_image(self, payload: Dict[str, Any]) -> str:
        """Generate image from description"""
        logger.info(f"Generating image: {payload.get('description', '')[:50]}...")
        # TODO: Replace with actual image generation
        time.sleep(0.1)  # Simulate processing
        return f"s3://bucket/images/{int(time.time())}.png"
    
    def generate_video(self, payload: Dict[str, Any]) -> str:
        """Generate video from description"""
        logger.info(f"Generating video: {payload.get('description', '')[:50]}...")
        # TODO: Replace with actual video generation
        time.sleep(0.2)  # Simulate processing
        return f"s3://bucket/videos/{int(time.time())}.mp4"
    
    def generate_voice(self, payload: Dict[str, Any]) -> str:
        """Generate voice/audio from description"""
        logger.info(f"Generating audio: {payload.get('description', '')[:50]}...")
        # TODO: Replace with actual voice generation
        time.sleep(0.1)  # Simulate processing
        return f"s3://bucket/audio/{int(time.time())}.wav"
    
    def generate_music(self, payload: Dict[str, Any]) -> str:
        """Generate background music"""
        logger.info("Generating background music...")
        # TODO: Replace with actual music generation
        time.sleep(0.1)  # Simulate processing
        return f"s3://bucket/music/{int(time.time())}.mp3"
    
    def compose_video(self, payload: Dict[str, Any]) -> str:
        """Compose final video from all shots"""
        logger.info("Composing final video...")
        # TODO: Replace with actual FFmpeg composition
        time.sleep(0.3)  # Simulate processing
        return f"s3://bucket/final/{int(time.time())}.mp4"


class Worker:
    """Autonomous worker that processes tasks from queue"""
    
    def __init__(self, worker_id: str):
        self.worker_id = worker_id
        self.task_queue = get_task_queue()
        self.job_store = get_job_store()
        self.orchestrator = get_orchestrator()
        self.model_executor = ModelExecutor()
        self.running = False
        self.current_task: Optional[TaskMessage] = None
    
    def start(self, max_tasks: Optional[int] = None) -> None:
        """
        Start worker loop
        
        Args:
            max_tasks: Maximum number of tasks to process (None = infinite)
        """
        self.running = True
        tasks_processed = 0
        
        logger.info(f"Worker {self.worker_id} started")
        
        while self.running:
            # Check if we've hit the task limit
            if max_tasks and tasks_processed >= max_tasks:
                logger.info(f"Worker {self.worker_id} reached task limit")
                break
            
            # Pull task from queue
            task = self.task_queue.dequeue()
            
            if not task:
                # No tasks available
                time.sleep(0.5)
                continue
            
            self.current_task = task
            
            try:
                # Process the task
                self._process_task(task)
                tasks_processed += 1
            except Exception as e:
                logger.error(f"Worker {self.worker_id} failed to process task {task.id}: {e}")
                self.task_queue.fail_task(task.id, str(e))
            finally:
                self.current_task = None
        
        logger.info(f"Worker {self.worker_id} stopped after processing {tasks_processed} tasks")
    
    def stop(self) -> None:
        """Stop worker"""
        self.running = False
        logger.info(f"Worker {self.worker_id} stopping...")
    
    def _process_task(self, task: TaskMessage) -> None:
        """Process a single task"""
        logger.info(f"Worker {self.worker_id} processing task {task.id} ({task.task_type})")
        
        try:
            # Load context
            shot = self.job_store.get_shot(task.shot_id)
            if not shot and task.task_type != TaskType.COMPOSITION:
                raise ValueError(f"Shot {task.shot_id} not found")
            
            # Update shot status
            if shot:
                shot.status = TaskStatus.RUNNING
                self.job_store.update_shot(shot)
            
            # Execute based on task type
            asset_url = None
            if task.task_type == TaskType.IMAGE_GENERATION:
                asset_url = self.model_executor.generate_image(task.payload)
            elif task.task_type == TaskType.VIDEO_GENERATION:
                asset_url = self.model_executor.generate_video(task.payload)
            elif task.task_type == TaskType.VOICE_GENERATION:
                asset_url = self.model_executor.generate_voice(task.payload)
            elif task.task_type == TaskType.MUSIC_GENERATION:
                asset_url = self.model_executor.generate_music(task.payload)
            elif task.task_type == TaskType.COMPOSITION:
                asset_url = self._compose_final_video(task)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            # Update storage with asset URL
            if shot and asset_url:
                shot.asset_url = asset_url
                shot.status = TaskStatus.COMPLETED
                self.job_store.update_shot(shot)
            
            # Mark task as complete
            self.task_queue.complete_task(task.id)
            
            # Update job progress
            self.orchestrator.update_progress(task.job_id)
            
            logger.info(f"Worker {self.worker_id} completed task {task.id}")
            
        except Exception as e:
            logger.error(f"Task {task.id} failed: {e}")
            
            # Update shot status
            if shot:
                shot.status = TaskStatus.FAILED
                self.job_store.update_shot(shot)
            
            # Handle retry
            retry_queued = self.task_queue.fail_task(task.id, str(e))
            
            if not retry_queued:
                # Task moved to DLQ, update job
                self.orchestrator.update_progress(task.job_id)
            
            raise
    
    def _compose_final_video(self, task: TaskMessage) -> str:
        """Compose final video from all shots"""
        job = self.job_store.get_job(task.job_id)
        if not job:
            raise ValueError(f"Job {task.job_id} not found")
        
        # Collect all shot assets
        all_shots = []
        for scene in job.scenes:
            for shot in scene.shots:
                if shot.asset_url:
                    all_shots.append({
                        "scene": scene.scene_number,
                        "shot": shot.shot_number,
                        "url": shot.asset_url,
                        "duration": shot.duration
                    })
        
        # Execute composition
        payload = {
            "shots": all_shots,
            "output_format": task.payload.get("output_format", "mp4")
        }
        
        final_url = self.model_executor.compose_video(payload)
        
        # Mark job as completed
        self.orchestrator.complete_job(job.id, final_url)
        
        return final_url


def create_worker(worker_id: Optional[str] = None) -> Worker:
    """Create a new worker instance"""
    if not worker_id:
        worker_id = f"worker-{int(time.time())}"
    return Worker(worker_id)

"""Workflow orchestration engine"""
from typing import Optional, List
from datetime import datetime
from src.models.workflow import (
    Job, Scene, Shot, JobStatus, TaskStatus, TaskType, TaskMessage, WorkflowState
)
from src.services.storage import get_job_store
from src.services.queue import get_task_queue
from src.services.script_parser import ScriptParser
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

# Constants
MIN_SCRIPT_LENGTH = 10  # Minimum characters for a valid script


class WorkflowOrchestrator:
    """Orchestrates the automated film production workflow"""
    
    def __init__(self):
        self.job_store = get_job_store()
        self.task_queue = get_task_queue()
        self.script_parser = ScriptParser()
    
    def create_job(self, user_id: str, script: str, title: Optional[str] = None) -> Job:
        """
        Create a new job and initiate the workflow
        
        Steps:
        1. Validate script
        2. Create job record
        3. Parse script into scenes/shots
        4. Estimate cost
        5. Build task graph
        6. Push tasks to queue
        """
        logger.info(f"Creating new job for user {user_id}")
        
        # Step 1: Validate script
        if not self._validate_script(script):
            raise ValueError("Invalid script content")
        
        # Step 2: Create job record
        job = Job(
            user_id=user_id,
            script=script,
            title=title or "Untitled Film",
            status=JobStatus.VALIDATING
        )
        job = self.job_store.create_job(job)
        
        # Step 3: Parse script into scenes and shots
        try:
            scenes = self.script_parser.parse_script(script, job.id)
            
            # Store scenes and shots
            for scene in scenes:
                self.job_store.add_scene(scene)
                for shot in scene.shots:
                    self.job_store.add_shot(shot)
            
            job.scenes = scenes
            logger.info(f"Parsed {len(scenes)} scenes for job {job.id}")
        except Exception as e:
            logger.error(f"Failed to parse script: {e}")
            job.status = JobStatus.FAILED
            job.error_message = f"Script parsing failed: {str(e)}"
            self.job_store.update_job(job)
            raise
        
        # Step 4: Estimate cost
        job.estimated_cost = self._estimate_cost(job)
        job.reserved_credits = job.estimated_cost
        
        # Step 5 & 6: Build task graph and push to queue
        try:
            tasks = self._build_task_graph(job)
            self.task_queue.enqueue_batch(tasks)
            
            job.status = JobStatus.QUEUED
            self.job_store.update_job(job)
            
            logger.info(f"Job {job.id} created with {len(tasks)} tasks")
            return job
        except Exception as e:
            logger.error(f"Failed to build task graph: {e}")
            job.status = JobStatus.FAILED
            job.error_message = f"Task graph creation failed: {str(e)}"
            self.job_store.update_job(job)
            raise
    
    def _validate_script(self, script: str) -> bool:
        """Validate script content"""
        if not script or not script.strip():
            return False
        
        # Basic validation - at least MIN_SCRIPT_LENGTH characters
        if len(script.strip()) < MIN_SCRIPT_LENGTH:
            return False
        
        # TODO: Add moderation check here
        return True
    
    def _estimate_cost(self, job: Job) -> float:
        """Estimate cost for job based on scenes and shots"""
        total_cost = 0.0
        
        # Base costs per task type
        costs = {
            TaskType.IMAGE_GENERATION: 0.10,
            TaskType.VIDEO_GENERATION: 0.50,
            TaskType.VOICE_GENERATION: 0.05,
            TaskType.MUSIC_GENERATION: 0.15,
            TaskType.COMPOSITION: 0.25
        }
        
        # Calculate shot costs
        for scene in job.scenes:
            for shot in scene.shots:
                # Each shot needs video + audio
                total_cost += costs[TaskType.VIDEO_GENERATION]
                total_cost += costs[TaskType.VOICE_GENERATION]
        
        # Add composition cost
        total_cost += costs[TaskType.COMPOSITION]
        
        logger.info(f"Estimated cost for job {job.id}: ${total_cost:.2f}")
        return total_cost
    
    def _build_task_graph(self, job: Job) -> List[TaskMessage]:
        """Build dependency graph of tasks"""
        tasks = []
        
        for scene in job.scenes:
            for shot in scene.shots:
                # Create video generation task for each shot
                video_task = TaskMessage(
                    job_id=job.id,
                    scene_id=scene.id,
                    shot_id=shot.id,
                    task_type=TaskType.VIDEO_GENERATION,
                    priority=scene.scene_number,
                    payload={
                        "description": shot.description,
                        "duration": shot.duration,
                        "camera_angle": shot.camera_angle,
                        "visual_context": shot.visual_context or {}
                    }
                )
                tasks.append(video_task)
                
                # Create audio task for each shot
                audio_task = TaskMessage(
                    job_id=job.id,
                    scene_id=scene.id,
                    shot_id=shot.id,
                    task_type=TaskType.VOICE_GENERATION,
                    priority=scene.scene_number,
                    payload={
                        "description": shot.description,
                        "duration": shot.duration,
                        "audio_context": shot.audio_context or {}
                    }
                )
                tasks.append(audio_task)
        
        logger.info(f"Built task graph with {len(tasks)} tasks for job {job.id}")
        return tasks
    
    def get_workflow_state(self, job_id: str) -> Optional[WorkflowState]:
        """Get current workflow state for a job"""
        job = self.job_store.get_job(job_id)
        if not job:
            return None
        
        total_scenes = len(job.scenes)
        total_shots = sum(len(scene.shots) for scene in job.scenes)
        completed_shots = sum(
            1 for scene in job.scenes 
            for shot in scene.shots 
            if shot.status == TaskStatus.COMPLETED
        )
        failed_shots = sum(
            1 for scene in job.scenes 
            for shot in scene.shots 
            if shot.status == TaskStatus.FAILED
        )
        completed_scenes = sum(
            1 for scene in job.scenes
            if all(shot.status == TaskStatus.COMPLETED for shot in scene.shots)
        )
        
        state = WorkflowState(
            job_id=job_id,
            current_status=job.status,
            total_scenes=total_scenes,
            completed_scenes=completed_scenes,
            total_shots=total_shots,
            completed_shots=completed_shots,
            failed_shots=failed_shots,
            pending_tasks=self.task_queue.get_queue_depth(),
            running_tasks=self.task_queue.get_processing_count()
        )
        
        return state
    
    def update_progress(self, job_id: str) -> None:
        """Update job progress based on completed shots"""
        job = self.job_store.get_job(job_id)
        if not job:
            return
        
        state = self.get_workflow_state(job_id)
        if not state:
            return
        
        if state.total_shots > 0:
            job.progress = (state.completed_shots / state.total_shots) * 100
        
        # Update job status based on state
        if state.completed_shots == state.total_shots and state.total_shots > 0:
            # All shots completed, trigger composition (only if not already composing/completed)
            if job.status not in [JobStatus.COMPOSING, JobStatus.COMPLETED]:
                job.status = JobStatus.COMPOSING
                self._trigger_composition(job)
        elif state.failed_shots > 0 and state.failed_shots == state.total_shots:
            # All shots failed
            job.status = JobStatus.FAILED
            job.error_message = "All shots failed to generate"
        elif state.completed_shots > 0 or state.running_tasks > 0:
            if job.status not in [JobStatus.COMPOSING, JobStatus.COMPLETED]:
                job.status = JobStatus.PROCESSING
        
        self.job_store.update_job(job)
    
    def _trigger_composition(self, job: Job) -> None:
        """Trigger final composition when all shots are complete"""
        logger.info(f"Triggering composition for job {job.id}")
        
        # Create composition task
        composition_task = TaskMessage(
            job_id=job.id,
            scene_id="composition",
            shot_id="final",
            task_type=TaskType.COMPOSITION,
            priority=999,  # High priority
            payload={
                "scenes": [scene.id for scene in job.scenes],
                "output_format": "mp4"
            }
        )
        
        self.task_queue.enqueue(composition_task)
    
    def complete_job(self, job_id: str, final_video_url: str) -> None:
        """Mark job as completed"""
        job = self.job_store.get_job(job_id)
        if not job:
            return
        
        job.status = JobStatus.COMPLETED
        job.final_video_url = final_video_url
        job.completed_at = datetime.utcnow()
        job.progress = 100.0
        
        self.job_store.update_job(job)
        logger.info(f"Job {job_id} completed successfully")
    
    def fail_job(self, job_id: str, error_message: str) -> None:
        """Mark job as failed"""
        job = self.job_store.get_job(job_id)
        if not job:
            return
        
        job.status = JobStatus.FAILED
        job.error_message = error_message
        job.completed_at = datetime.utcnow()
        
        self.job_store.update_job(job)
        logger.error(f"Job {job_id} failed: {error_message}")


# Global orchestrator instance
_orchestrator = WorkflowOrchestrator()


def get_orchestrator() -> WorkflowOrchestrator:
    """Get the global orchestrator instance"""
    return _orchestrator

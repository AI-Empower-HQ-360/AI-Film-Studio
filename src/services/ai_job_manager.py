"""
AI Job Management Service
Handles job queuing, scheduling, and GPU resource allocation
"""
from typing import Optional, Dict, Any, List
from enum import Enum
import asyncio
import logging
import uuid
from datetime import datetime

try:
    from pydantic import BaseModel, Field
    HAS_PYDANTIC = True
except ImportError:
    # Fallback for testing without pydantic
    HAS_PYDANTIC = False
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    def Field(*args, **kwargs):
        return None

try:
    from ..config.ai_models import (
        JOB_QUEUE_CONFIG,
        GPU_INSTANCE_CONFIGS,
        get_recommended_gpu_instance
    )
except ImportError:
    # Fallback for testing
    JOB_QUEUE_CONFIG = {}
    GPU_INSTANCE_CONFIGS = {}
    def get_recommended_gpu_instance(job_type: str) -> str:
        return "g4dn.xlarge"

logger = logging.getLogger(__name__)


class JobType(str, Enum):
    """AI Job Types"""
    VIDEO_GENERATION = "video_generation"
    VOICE_SYNTHESIS = "voice_synthesis"
    LIPSYNC_ANIMATION = "lipsync_animation"
    MUSIC_GENERATION = "music_generation"
    PODCAST_VIDEO = "podcast_video"
    SUBTITLE_GENERATION = "subtitle_generation"


class JobPriority(str, Enum):
    """Job Priority Levels"""
    CRITICAL = "critical"  # Enterprise users
    HIGH = "high"  # Pro users
    MEDIUM = "medium"  # Free users
    LOW = "low"  # Background jobs


class JobStatus(str, Enum):
    """Job Status"""
    SUBMITTED = "submitted"
    QUEUED = "queued"
    PROCESSING = "processing"
    RENDERING = "rendering"
    POST_PROCESSING = "post_processing"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobSubmissionRequest(BaseModel):
    """Request model for job submission"""
    job_type: JobType
    priority: JobPriority = JobPriority.MEDIUM
    user_id: str
    parameters: Dict[str, Any] = Field(..., description="Job-specific parameters")
    callback_url: Optional[str] = Field(default=None, description="Webhook for completion")
    max_retries: int = Field(default=3, ge=0, le=5)


class JobStatusResponse(BaseModel):
    """Response model for job status"""
    job_id: str
    job_type: JobType
    status: JobStatus
    priority: JobPriority
    progress: float = Field(default=0.0, ge=0.0, le=100.0, description="Progress percentage")
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_completion: Optional[datetime] = None
    worker_id: Optional[str] = None
    gpu_instance: Optional[str] = None
    retry_count: int = 0
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None


class WorkerInfo(BaseModel):
    """Worker node information"""
    worker_id: str
    gpu_instance: str
    status: str  # idle, busy, offline
    current_job_id: Optional[str] = None
    total_jobs_processed: int = 0
    uptime: float
    gpu_utilization: float = 0.0
    gpu_memory_used: float = 0.0


class AIJobManager:
    """Service for managing AI processing jobs and GPU workers"""
    
    def __init__(
        self,
        queue_service: str = "aws_sqs",  # aws_sqs, bullmq, rabbitmq
        auto_scaling: bool = True
    ):
        self.queue_service = queue_service
        self.auto_scaling = auto_scaling
        
        # Job storage
        self.jobs: Dict[str, JobStatusResponse] = {}
        self.job_queue: Dict[JobPriority, List[str]] = {
            JobPriority.CRITICAL: [],
            JobPriority.HIGH: [],
            JobPriority.MEDIUM: [],
            JobPriority.LOW: []
        }
        
        # Worker storage
        self.workers: Dict[str, WorkerInfo] = {}
        self.worker_queue: List[str] = []  # Available workers
    
    async def submit_job(
        self,
        request: JobSubmissionRequest
    ) -> JobStatusResponse:
        """
        Submit a new AI processing job
        
        Args:
            request: Job submission request
            
        Returns:
            JobStatusResponse with job details
        """
        try:
            # Generate job ID
            job_id = str(uuid.uuid4())
            
            logger.info(f"Submitting job {job_id} of type {request.job_type}")
            
            # Create job status
            job_status = JobStatusResponse(
                job_id=job_id,
                job_type=request.job_type,
                status=JobStatus.SUBMITTED,
                priority=request.priority,
                created_at=datetime.utcnow()
            )
            
            # Store job
            self.jobs[job_id] = job_status
            
            # Add to priority queue
            self.job_queue[request.priority].append(job_id)
            
            # Update status to queued
            job_status.status = JobStatus.QUEUED
            
            # Trigger worker assignment if available
            await self._assign_worker_to_job()
            
            # Trigger auto-scaling check
            if self.auto_scaling:
                await self._check_auto_scaling()
            
            logger.info(f"Job {job_id} submitted successfully")
            
            return job_status
            
        except Exception as e:
            logger.error(f"Error submitting job: {str(e)}")
            raise
    
    async def get_job_status(self, job_id: str) -> JobStatusResponse:
        """Get status of a specific job"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        return self.jobs[job_id]
    
    async def cancel_job(self, job_id: str) -> bool:
        """Cancel a job"""
        if job_id not in self.jobs:
            return False
        
        job = self.jobs[job_id]
        
        # Can only cancel queued or processing jobs
        if job.status not in [JobStatus.QUEUED, JobStatus.PROCESSING]:
            return False
        
        # Update status
        job.status = JobStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        
        # Remove from queue if queued
        for priority_queue in self.job_queue.values():
            if job_id in priority_queue:
                priority_queue.remove(job_id)
        
        # If processing, notify worker to stop
        if job.worker_id:
            await self._notify_worker_cancel(job.worker_id, job_id)
        
        logger.info(f"Job {job_id} cancelled")
        return True
    
    async def list_jobs(
        self,
        user_id: Optional[str] = None,
        status: Optional[JobStatus] = None,
        limit: int = 50
    ) -> List[JobStatusResponse]:
        """List jobs with optional filters"""
        jobs = list(self.jobs.values())
        
        # Apply filters
        if user_id:
            # TODO: Filter by user_id (need to store in JobStatusResponse)
            pass
        
        if status:
            jobs = [j for j in jobs if j.status == status]
        
        # Sort by created_at descending
        jobs.sort(key=lambda j: j.created_at, reverse=True)
        
        return jobs[:limit]
    
    async def register_worker(
        self,
        worker_id: str,
        gpu_instance: str
    ) -> WorkerInfo:
        """Register a new worker node"""
        logger.info(f"Registering worker {worker_id} with GPU {gpu_instance}")
        
        worker = WorkerInfo(
            worker_id=worker_id,
            gpu_instance=gpu_instance,
            status="idle",
            total_jobs_processed=0,
            uptime=0.0
        )
        
        self.workers[worker_id] = worker
        self.worker_queue.append(worker_id)
        
        # Try to assign job to new worker
        await self._assign_worker_to_job()
        
        return worker
    
    async def update_worker_status(
        self,
        worker_id: str,
        status: str,
        gpu_utilization: Optional[float] = None,
        gpu_memory_used: Optional[float] = None
    ):
        """Update worker status and metrics"""
        if worker_id not in self.workers:
            raise ValueError(f"Worker {worker_id} not found")
        
        worker = self.workers[worker_id]
        worker.status = status
        
        if gpu_utilization is not None:
            worker.gpu_utilization = gpu_utilization
        
        if gpu_memory_used is not None:
            worker.gpu_memory_used = gpu_memory_used
        
        # If worker becomes idle, try to assign next job
        if status == "idle" and worker_id not in self.worker_queue:
            self.worker_queue.append(worker_id)
            await self._assign_worker_to_job()
    
    async def report_job_progress(
        self,
        job_id: str,
        progress: float,
        status: Optional[JobStatus] = None
    ):
        """Update job progress"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        job.progress = min(100.0, max(0.0, progress))
        
        if status:
            job.status = status
            
            if status == JobStatus.PROCESSING and not job.started_at:
                job.started_at = datetime.utcnow()
            
            if status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
                job.completed_at = datetime.utcnow()
                
                # Free up worker
                if job.worker_id and job.worker_id in self.workers:
                    await self.update_worker_status(job.worker_id, "idle")
    
    async def complete_job(
        self,
        job_id: str,
        result: Dict[str, Any]
    ):
        """Mark job as completed with result"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        job.status = JobStatus.COMPLETED
        job.progress = 100.0
        job.completed_at = datetime.utcnow()
        job.result = result
        
        # Update worker stats
        if job.worker_id and job.worker_id in self.workers:
            worker = self.workers[job.worker_id]
            worker.total_jobs_processed += 1
            await self.update_worker_status(job.worker_id, "idle")
        
        logger.info(f"Job {job_id} completed successfully")
    
    async def fail_job(
        self,
        job_id: str,
        error_message: str,
        retry: bool = True
    ):
        """Mark job as failed"""
        if job_id not in self.jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job = self.jobs[job_id]
        job.error_message = error_message
        
        # Check if we should retry
        job_config = JOB_QUEUE_CONFIG.get(job.job_type.value, {})
        max_retries = job_config.get("retry_count", 3)
        
        if retry and job.retry_count < max_retries:
            # Retry job
            job.retry_count += 1
            job.status = JobStatus.QUEUED
            job.worker_id = None
            
            # Add back to queue
            self.job_queue[job.priority].append(job_id)
            
            logger.info(f"Job {job_id} failed, retrying ({job.retry_count}/{max_retries})")
        else:
            # Mark as failed
            job.status = JobStatus.FAILED
            job.completed_at = datetime.utcnow()
            logger.error(f"Job {job_id} failed permanently: {error_message}")
        
        # Free up worker
        if job.worker_id and job.worker_id in self.workers:
            await self.update_worker_status(job.worker_id, "idle")
    
    async def _assign_worker_to_job(self):
        """Assign available workers to queued jobs"""
        if not self.worker_queue:
            return
        
        # Process queues by priority
        for priority in [JobPriority.CRITICAL, JobPriority.HIGH, 
                         JobPriority.MEDIUM, JobPriority.LOW]:
            while self.job_queue[priority] and self.worker_queue:
                job_id = self.job_queue[priority].pop(0)
                worker_id = self.worker_queue.pop(0)
                
                job = self.jobs[job_id]
                worker = self.workers[worker_id]
                
                # Assign job to worker
                job.status = JobStatus.PROCESSING
                job.worker_id = worker_id
                job.gpu_instance = worker.gpu_instance
                job.started_at = datetime.utcnow()
                
                worker.status = "busy"
                worker.current_job_id = job_id
                
                logger.info(f"Assigned job {job_id} to worker {worker_id}")
                
                # Notify worker (send via queue/webhook)
                await self._notify_worker_start(worker_id, job_id)
    
    async def _notify_worker_start(self, worker_id: str, job_id: str):
        """Notify worker to start processing job"""
        # TODO: Implement worker notification via SQS/RabbitMQ/BullMQ
        logger.info(f"Notifying worker {worker_id} to start job {job_id}")
    
    async def _notify_worker_cancel(self, worker_id: str, job_id: str):
        """Notify worker to cancel job"""
        # TODO: Implement worker cancellation notification
        logger.info(f"Notifying worker {worker_id} to cancel job {job_id}")
    
    async def _check_auto_scaling(self):
        """Check if we need to scale workers up or down"""
        if not self.auto_scaling:
            return
        
        # Count queued jobs by priority
        total_queued = sum(len(queue) for queue in self.job_queue.values())
        high_priority_queued = (
            len(self.job_queue[JobPriority.CRITICAL]) + 
            len(self.job_queue[JobPriority.HIGH])
        )
        
        # Count active workers
        active_workers = sum(1 for w in self.workers.values() if w.status != "offline")
        
        # Scale up if needed
        if total_queued > active_workers * 2:
            await self._scale_up_workers(1)
        
        # Scale down if idle
        idle_workers = sum(1 for w in self.workers.values() if w.status == "idle")
        if idle_workers > 3 and total_queued == 0:
            await self._scale_down_workers(1)
    
    async def _scale_up_workers(self, count: int):
        """Scale up worker count"""
        logger.info(f"Scaling up {count} workers")
        # TODO: Implement AWS EC2/ECS scaling
    
    async def _scale_down_workers(self, count: int):
        """Scale down worker count"""
        logger.info(f"Scaling down {count} workers")
        # TODO: Implement AWS EC2/ECS scaling
    
    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics"""
        return {
            "total_jobs": len(self.jobs),
            "queued_by_priority": {
                priority.value: len(queue)
                for priority, queue in self.job_queue.items()
            },
            "total_workers": len(self.workers),
            "active_workers": sum(1 for w in self.workers.values() if w.status == "busy"),
            "idle_workers": sum(1 for w in self.workers.values() if w.status == "idle"),
            "job_stats": {
                "completed": sum(1 for j in self.jobs.values() if j.status == JobStatus.COMPLETED),
                "failed": sum(1 for j in self.jobs.values() if j.status == JobStatus.FAILED),
                "processing": sum(1 for j in self.jobs.values() if j.status == JobStatus.PROCESSING),
                "queued": sum(1 for j in self.jobs.values() if j.status == JobStatus.QUEUED)
            }
        }
    
    def get_gpu_recommendations(self) -> Dict[str, Any]:
        """Get GPU instance recommendations"""
        return {
            "instances": GPU_INSTANCE_CONFIGS,
            "recommendations": {
                job_type: get_recommended_gpu_instance(job_type)
                for job_type in [jt.value for jt in JobType]
            }
        }

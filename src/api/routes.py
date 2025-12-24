"""API routes for film production workflow"""
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from src.models.workflow import Job, JobStatus, WorkflowState
from src.services.orchestrator import get_orchestrator
from src.services.storage import get_job_store
from src.services.worker import create_worker
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/api/v1", tags=["workflow"])


class ScriptSubmission(BaseModel):
    """Request model for script submission"""
    user_id: str = Field(..., description="User ID")
    script: str = Field(..., description="Film script content")
    title: Optional[str] = Field(None, description="Film title")


class JobResponse(BaseModel):
    """Response model for job"""
    id: str
    user_id: str
    title: Optional[str]
    status: JobStatus
    progress: float
    estimated_cost: float
    final_video_url: Optional[str]
    error_message: Optional[str]
    created_at: str
    
    @classmethod
    def from_job(cls, job: Job):
        return cls(
            id=job.id,
            user_id=job.user_id,
            title=job.title,
            status=job.status,
            progress=job.progress,
            estimated_cost=job.estimated_cost,
            final_video_url=job.final_video_url,
            error_message=job.error_message,
            created_at=job.created_at.isoformat()
        )


def start_worker_background():
    """Start a worker in the background"""
    worker = create_worker()
    worker.start(max_tasks=100)  # Process up to 100 tasks


@router.post("/jobs", response_model=JobResponse)
async def create_job(submission: ScriptSubmission, background_tasks: BackgroundTasks):
    """
    Create a new film production job
    
    This endpoint:
    1. Validates the script
    2. Creates a job record
    3. Parses script into scenes/shots
    4. Estimates cost
    5. Queues tasks for processing
    6. Starts a background worker
    
    The workflow is fully automated from this point.
    """
    try:
        orchestrator = get_orchestrator()
        
        # Create job and initiate workflow
        job = orchestrator.create_job(
            user_id=submission.user_id,
            script=submission.script,
            title=submission.title
        )
        
        # Start worker in background to process tasks
        background_tasks.add_task(start_worker_background)
        
        logger.info(f"Job {job.id} created and worker started")
        
        return JobResponse.from_job(job)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create job: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """Get job status and details"""
    job_store = get_job_store()
    job = job_store.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobResponse.from_job(job)


@router.get("/jobs/{job_id}/state", response_model=WorkflowState)
async def get_job_state(job_id: str):
    """Get detailed workflow state for a job"""
    orchestrator = get_orchestrator()
    state = orchestrator.get_workflow_state(job_id)
    
    if not state:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return state


@router.get("/jobs/{job_id}/download")
async def get_download_url(job_id: str):
    """
    Get signed download URL for completed job
    
    In production, this would generate a time-limited signed URL
    """
    job_store = get_job_store()
    job = job_store.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=400, 
            detail=f"Job not completed yet (status: {job.status})"
        )
    
    if not job.final_video_url:
        raise HTTPException(status_code=500, detail="Final video URL not available")
    
    # In production, generate signed URL here
    return {
        "download_url": job.final_video_url,
        "expires_in": 3600,  # 1 hour
        "job_id": job.id
    }


@router.get("/jobs")
async def list_jobs(user_id: Optional[str] = None):
    """List all jobs, optionally filtered by user"""
    job_store = get_job_store()
    jobs = job_store.list_jobs(user_id=user_id)
    
    return {
        "jobs": [JobResponse.from_job(job) for job in jobs],
        "total": len(jobs)
    }


@router.post("/jobs/{job_id}/cancel")
async def cancel_job(job_id: str):
    """Cancel a job (if still in progress)"""
    job_store = get_job_store()
    job = job_store.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel job in status: {job.status}"
        )
    
    job.status = JobStatus.CANCELLED
    job_store.update_job(job)
    
    return {"message": "Job cancelled", "job_id": job_id}

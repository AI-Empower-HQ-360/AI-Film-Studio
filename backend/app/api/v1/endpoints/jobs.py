"""
Jobs API endpoints.
"""
from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends

from ...schemas import JobCreate, JobUpdate, JobResponse, CostEstimate, SignedURLRequest, SignedURLResponse
from ...core.security import get_current_user
from ...services import (
    JobStateMachine, moderator, cost_governance, s3_service
)
from ...core.config import settings

router = APIRouter()

# Mock database for demonstration
mock_jobs = {}
job_counter = 0


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new job."""
    global job_counter
    job_counter += 1
    
    # Estimate cost
    job_config = job_data.config or {}
    cost_estimate = cost_governance.estimate_job_cost(job_config)
    estimated_cost = cost_estimate["total"]
    
    # Check cost limits
    is_allowed, reason = cost_governance.check_job_cost_limit(estimated_cost)
    if not is_allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=reason
        )
    
    # Moderate script
    if settings.ENABLE_CONTENT_MODERATION:
        moderation_result = moderator.moderate_text(job_data.script)
        if not moderation_result.is_approved:
            moderation_status = "rejected"
        else:
            moderation_status = "approved"
    else:
        moderation_result = None
        moderation_status = "skipped"
    
    job = {
        "id": job_counter,
        "project_id": job_data.project_id,
        "user_id": int(current_user["user_id"]),
        "script": job_data.script,
        "status": "pending",
        "progress": 0.0,
        "estimated_cost": estimated_cost,
        "actual_cost": 0.0,
        "moderation_status": moderation_status,
        "moderation_score": moderation_result.score if moderation_result else None,
        "output_url": None,
        "signed_url": None,
        "signed_url_expires_at": None,
        "error_message": None,
        "retry_count": 0,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "started_at": None,
        "completed_at": None
    }
    
    mock_jobs[job_counter] = job
    return JobResponse(**job)


@router.get("/", response_model=List[JobResponse])
async def list_jobs(current_user: dict = Depends(get_current_user)):
    """List all jobs for the current user."""
    user_id = int(current_user["user_id"])
    user_jobs = [
        JobResponse(**j) 
        for j in mock_jobs.values() 
        if j["user_id"] == user_id
    ]
    return user_jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Get a specific job."""
    job = mock_jobs.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check ownership
    if job["user_id"] != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this job"
        )
    
    return JobResponse(**job)


@router.patch("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update job status/progress."""
    job = mock_jobs.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check ownership
    if job["user_id"] != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this job"
        )
    
    # Update status with state machine validation
    if job_data.status:
        state_machine = JobStateMachine(job["status"])
        try:
            transition_info = state_machine.transition_to(job_data.status)
            job["status"] = job_data.status
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    # Update progress
    if job_data.progress is not None:
        job["progress"] = job_data.progress
    
    job["updated_at"] = datetime.utcnow().isoformat()
    
    return JobResponse(**job)


@router.post("/{job_id}/cancel", response_model=JobResponse)
async def cancel_job(
    job_id: int,
    current_user: dict = Depends(get_current_user)
):
    """Cancel a job."""
    job = mock_jobs.get(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check ownership
    if job["user_id"] != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this job"
        )
    
    # Transition to cancelled
    state_machine = JobStateMachine(job["status"])
    try:
        state_machine.transition_to("cancelled")
        job["status"] = "cancelled"
        job["updated_at"] = datetime.utcnow().isoformat()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return JobResponse(**job)


@router.post("/estimate-cost", response_model=CostEstimate)
async def estimate_cost(
    config: dict,
    current_user: dict = Depends(get_current_user)
):
    """Estimate cost for a job configuration."""
    cost_estimate = cost_governance.estimate_job_cost(config)
    return CostEstimate(
        estimated_cost=cost_estimate["total"],
        breakdown=cost_estimate["breakdown"]
    )


@router.post("/signed-url", response_model=SignedURLResponse)
async def get_signed_url(
    request: SignedURLRequest,
    current_user: dict = Depends(get_current_user)
):
    """Get signed URL for job output download."""
    job = mock_jobs.get(request.job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check ownership
    if job["user_id"] != int(current_user["user_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this job"
        )
    
    # Check if job is completed
    if job["status"] != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job not completed yet"
        )
    
    # Generate signed URL
    object_key = f"outputs/job_{request.job_id}/output.mp4"
    signed_url, expires_at = s3_service.generate_signed_url(object_key)
    
    if not signed_url:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate signed URL"
        )
    
    # Update job with signed URL info
    job["signed_url"] = signed_url
    job["signed_url_expires_at"] = expires_at.isoformat()
    
    return SignedURLResponse(url=signed_url, expires_at=expires_at)

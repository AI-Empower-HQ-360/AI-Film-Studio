from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime
from app.models.database import get_db
from app.models.models import Job, Project
from app.schemas.job import JobCreate, JobResponse, JobStatusUpdate
from app.core.security import get_current_user
from app.services.job_service import job_service
from app.services.storage import storage_service
from app.core.state_machine import JobStatus

router = APIRouter()


@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job"""
    # Verify project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == job.project_id,
        Project.user_id == current_user["user_id"]
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Create new job
    new_job = Job(
        id=str(uuid.uuid4()),
        user_id=current_user["user_id"],
        project_id=job.project_id,
        status=JobStatus.PENDING.value,
        progress=0,
        config=job.config or {}
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    # TODO: Queue job for worker processing
    
    return new_job


@router.get("/", response_model=List[JobResponse])
async def list_jobs(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    project_id: str = Query(None, description="Filter by project ID"),
    status: str = Query(None, description="Filter by status"),
    skip: int = 0,
    limit: int = 100
):
    """List user's jobs"""
    query = db.query(Job).filter(Job.user_id == current_user["user_id"])
    
    if project_id:
        query = query.filter(Job.project_id == project_id)
    
    if status:
        query = query.filter(Job.status == status)
    
    jobs = query.offset(skip).limit(limit).all()
    return jobs


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific job"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user["user_id"]
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return job


@router.patch("/{job_id}/status", response_model=JobResponse)
async def update_job_status(
    job_id: str,
    status_update: JobStatusUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update job status (with state machine validation)"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user["user_id"]
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        new_status = JobStatus(status_update.status)
        updated_job = job_service.update_job_status(
            db=db,
            job_id=job_id,
            new_status=new_status,
            progress=status_update.progress,
            error_message=status_update.error_message
        )
        return updated_job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{job_id}/cancel", response_model=JobResponse)
async def cancel_job(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a job"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user["user_id"]
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        updated_job = job_service.update_job_status(
            db=db,
            job_id=job_id,
            new_status=JobStatus.CANCELLED
        )
        return updated_job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{job_id}/download-url")
async def get_download_url(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a signed URL for downloading job output"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user["user_id"]
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != JobStatus.COMPLETED.value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job is not completed yet"
        )
    
    if not job.output_video_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Output video not available"
        )
    
    # Generate signed URL for download
    object_key = f"jobs/{job_id}/output.mp4"
    signed_url = storage_service.generate_download_url(object_key)
    
    return {
        "download_url": signed_url,
        "expires_in": 3600
    }


@router.get("/{job_id}/valid-transitions")
async def get_valid_transitions(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get valid state transitions for a job"""
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user["user_id"]
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    next_states = job_service.get_next_valid_states(job.status)
    
    return {
        "current_status": job.status,
        "valid_transitions": next_states
    }

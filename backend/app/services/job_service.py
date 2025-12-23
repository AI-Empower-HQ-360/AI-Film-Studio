from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Job
from app.core.state_machine import JobStatus, JobTransitions
from typing import Optional


class JobService:
    """Service for managing job state machine and transitions"""
    
    @staticmethod
    def update_job_status(
        db: Session,
        job_id: str,
        new_status: JobStatus,
        progress: Optional[int] = None,
        error_message: Optional[str] = None
    ) -> Job:
        """
        Update job status with state machine validation
        
        Args:
            db: Database session
            job_id: Job ID
            new_status: New status to transition to
            progress: Optional progress percentage
            error_message: Optional error message for failed jobs
            
        Returns:
            Updated job object
            
        Raises:
            ValueError: If transition is invalid
        """
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise ValueError(f"Job {job_id} not found")
        
        current_status = JobStatus(job.status)
        
        # Validate transition
        if not JobTransitions.can_transition(current_status, new_status):
            raise ValueError(
                f"Invalid state transition from {current_status} to {new_status}"
            )
        
        # Update job
        job.status = new_status.value
        job.updated_at = datetime.utcnow()
        
        if progress is not None:
            job.progress = progress
        
        if error_message:
            job.error_message = error_message
        
        # Update timestamps based on status
        if new_status == JobStatus.PROCESSING and not job.started_at:
            job.started_at = datetime.utcnow()
        
        if new_status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            job.completed_at = datetime.utcnow()
        
        db.commit()
        db.refresh(job)
        return job
    
    @staticmethod
    def get_next_valid_states(job_status: str) -> list[str]:
        """Get list of valid next states for a job"""
        current = JobStatus(job_status)
        return [s.value for s in JobTransitions.get_next_states(current)]


job_service = JobService()

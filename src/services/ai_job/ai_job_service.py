"""
AI Job Service - Handles AI processing job queue and status management
"""
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class JobType(str, Enum):
    """Job types for AI processing"""
    SCRIPT_ANALYSIS = "script_analysis"
    IMAGE_GENERATION = "image_generation"
    VOICE_SYNTHESIS = "voice_synthesis"
    VIDEO_COMPOSITION = "video_composition"
    SUBTITLE_GENERATION = "subtitle_generation"
    THUMBNAIL_GENERATION = "thumbnail_generation"
    FULL_GENERATION = "full_generation"


class JobStatus(str, Enum):
    """Job status states"""
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobPriority(int, Enum):
    """Job priority levels"""
    LOW = 1  # Free users
    NORMAL = 2  # Pro users
    HIGH = 3  # Enterprise users


class AIJobService:
    """Service for managing AI processing jobs"""
    
    def __init__(self, db_connection, queue_client):
        self.db = db_connection
        self.queue = queue_client
    
    async def create_job(
        self,
        project_id: str,
        user_id: str,
        job_type: str,
        parameters: Dict,
        priority: int = JobPriority.NORMAL
    ) -> Dict:
        """
        Create a new AI processing job
        
        Args:
            project_id: Project ID
            user_id: User ID
            job_type: Type of job to create
            parameters: Job-specific parameters
            priority: Job priority (1=low, 2=normal, 3=high)
            
        Returns:
            Created job information
        """
        try:
            # Validate job type
            if job_type not in [jt.value for jt in JobType]:
                raise ValueError(f"Invalid job type: {job_type}")
            
            # Create job record in database
            job_data = {
                "project_id": project_id,
                "user_id": user_id,
                "type": job_type,
                "status": JobStatus.QUEUED.value,
                "progress": 0,
                "parameters": parameters,
                "priority": priority,
                "retry_count": 0,
                "max_retries": 3
            }
            
            job_id = await self.db.insert("jobs", job_data)
            
            # Enqueue job for processing
            await self.queue.enqueue({
                "job_id": job_id,
                "project_id": project_id,
                "user_id": user_id,
                "type": job_type,
                "parameters": parameters,
                "priority": priority
            }, priority=priority)
            
            logger.info(f"Job created: {job_id} (type: {job_type})")
            
            return await self.get_job(job_id)
            
        except Exception as e:
            logger.error(f"Error creating job: {str(e)}")
            raise
    
    async def get_job(self, job_id: str) -> Optional[Dict]:
        """Get job by ID"""
        try:
            jobs = await self.db.query(
                "SELECT * FROM jobs WHERE id = %s",
                (job_id,)
            )
            return jobs[0] if jobs else None
        except Exception as e:
            logger.error(f"Error fetching job: {str(e)}")
            raise
    
    async def get_user_jobs(
        self,
        user_id: str,
        status: Optional[str] = None,
        limit: int = 20,
        offset: int = 0
    ) -> List[Dict]:
        """Get all jobs for a user"""
        try:
            query = "SELECT * FROM jobs WHERE user_id = %s"
            params = [user_id]
            
            if status:
                query += " AND status = %s"
                params.append(status)
            
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            jobs = await self.db.query(query, tuple(params))
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching user jobs: {str(e)}")
            raise
    
    async def get_project_jobs(self, project_id: str) -> List[Dict]:
        """Get all jobs for a project"""
        try:
            jobs = await self.db.query(
                "SELECT * FROM jobs WHERE project_id = %s ORDER BY created_at DESC",
                (project_id,)
            )
            return jobs
        except Exception as e:
            logger.error(f"Error fetching project jobs: {str(e)}")
            raise
    
    async def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: Optional[int] = None,
        current_step: Optional[str] = None,
        error_message: Optional[str] = None,
        error_details: Optional[Dict] = None
    ) -> Dict:
        """
        Update job status and progress
        
        Args:
            job_id: Job ID
            status: New status
            progress: Progress percentage (0-100)
            current_step: Current processing step description
            error_message: Error message (if failed)
            error_details: Detailed error information
            
        Returns:
            Updated job information
        """
        try:
            updates = {"status": status}
            
            if progress is not None:
                updates["progress"] = progress
            
            if current_step:
                updates["current_step"] = current_step
            
            if error_message:
                updates["error_message"] = error_message
            
            if error_details:
                updates["error_details"] = error_details
            
            # Set timestamp based on status
            if status == JobStatus.PROCESSING.value and "started_at" not in updates:
                updates["started_at"] = datetime.utcnow()
            elif status == JobStatus.COMPLETED.value:
                updates["completed_at"] = datetime.utcnow()
            elif status == JobStatus.FAILED.value:
                updates["failed_at"] = datetime.utcnow()
            
            await self.db.update("jobs", {"id": job_id}, updates)
            
            logger.info(f"Job status updated: {job_id} -> {status}")
            
            return await self.get_job(job_id)
            
        except Exception as e:
            logger.error(f"Error updating job status: {str(e)}")
            raise
    
    async def update_job_result(
        self,
        job_id: str,
        result: Dict,
        output_url: Optional[str] = None
    ) -> Dict:
        """
        Update job with result data
        
        Args:
            job_id: Job ID
            result: Job result data
            output_url: URL to output file
            
        Returns:
            Updated job information
        """
        try:
            updates = {
                "result": result,
                "status": JobStatus.COMPLETED.value,
                "progress": 100,
                "completed_at": datetime.utcnow()
            }
            
            if output_url:
                updates["output_url"] = output_url
            
            await self.db.update("jobs", {"id": job_id}, updates)
            
            logger.info(f"Job result updated: {job_id}")
            
            return await self.get_job(job_id)
            
        except Exception as e:
            logger.error(f"Error updating job result: {str(e)}")
            raise
    
    async def cancel_job(self, job_id: str, user_id: str) -> bool:
        """
        Cancel a job
        
        Args:
            job_id: Job ID
            user_id: User ID (for authorization)
            
        Returns:
            True if successful
        """
        try:
            job = await self.get_job(job_id)
            
            if not job or job["user_id"] != user_id:
                raise ValueError("Job not found or unauthorized")
            
            if job["status"] not in [JobStatus.QUEUED.value, JobStatus.PROCESSING.value]:
                raise ValueError("Job cannot be cancelled in current status")
            
            await self.update_job_status(job_id, JobStatus.CANCELLED.value)
            
            # Remove from queue if queued
            if job["status"] == JobStatus.QUEUED.value:
                await self.queue.remove(job_id)
            
            logger.info(f"Job cancelled: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling job: {str(e)}")
            raise
    
    async def retry_job(self, job_id: str) -> Dict:
        """
        Retry a failed job
        
        Args:
            job_id: Job ID
            
        Returns:
            Updated job information
        """
        try:
            job = await self.get_job(job_id)
            
            if not job:
                raise ValueError("Job not found")
            
            if job["status"] != JobStatus.FAILED.value:
                raise ValueError("Only failed jobs can be retried")
            
            if job["retry_count"] >= job["max_retries"]:
                raise ValueError("Maximum retry attempts exceeded")
            
            # Increment retry count
            retry_count = job["retry_count"] + 1
            
            # Reset job status
            updates = {
                "status": JobStatus.QUEUED.value,
                "progress": 0,
                "retry_count": retry_count,
                "error_message": None,
                "error_details": None
            }
            
            await self.db.update("jobs", {"id": job_id}, updates)
            
            # Re-enqueue job
            await self.queue.enqueue({
                "job_id": job_id,
                "project_id": job["project_id"],
                "user_id": job["user_id"],
                "type": job["type"],
                "parameters": job["parameters"],
                "priority": job["priority"],
                "retry_count": retry_count
            }, priority=job["priority"])
            
            logger.info(f"Job retried: {job_id} (attempt {retry_count})")
            
            return await self.get_job(job_id)
            
        except Exception as e:
            logger.error(f"Error retrying job: {str(e)}")
            raise
    
    async def get_queue_stats(self) -> Dict:
        """Get queue statistics"""
        try:
            stats = await self.db.query(
                """
                SELECT 
                    status,
                    COUNT(*) as count,
                    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) as avg_duration
                FROM jobs
                WHERE created_at > NOW() - INTERVAL '24 hours'
                GROUP BY status
                """
            )
            
            return {
                "stats": stats,
                "queue_depth": await self.queue.get_queue_depth()
            }
            
        except Exception as e:
            logger.error(f"Error fetching queue stats: {str(e)}")
            raise

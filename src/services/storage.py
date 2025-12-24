"""In-memory storage for jobs, scenes, and shots"""
from typing import Optional, List, Dict
from datetime import datetime
from src.models.workflow import Job, Scene, Shot, JobStatus, TaskStatus
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class JobStore:
    """In-memory job storage"""
    
    def __init__(self):
        self._jobs: Dict[str, Job] = {}
        self._scenes: Dict[str, Scene] = {}
        self._shots: Dict[str, Shot] = {}
    
    def create_job(self, job: Job) -> Job:
        """Create a new job"""
        self._jobs[job.id] = job
        logger.info(f"Created job {job.id} for user {job.user_id}")
        return job
    
    def get_job(self, job_id: str) -> Optional[Job]:
        """Get job by ID"""
        return self._jobs.get(job_id)
    
    def update_job(self, job: Job) -> Job:
        """Update job"""
        job.updated_at = datetime.utcnow()
        self._jobs[job.id] = job
        return job
    
    def list_jobs(self, user_id: Optional[str] = None) -> List[Job]:
        """List all jobs, optionally filtered by user"""
        jobs = list(self._jobs.values())
        if user_id:
            jobs = [j for j in jobs if j.user_id == user_id]
        return sorted(jobs, key=lambda x: x.created_at, reverse=True)
    
    def add_scene(self, scene: Scene) -> Scene:
        """Add a scene to storage"""
        self._scenes[scene.id] = scene
        
        # Update job's scenes list
        job = self.get_job(scene.job_id)
        if job:
            if scene not in job.scenes:
                job.scenes.append(scene)
                self.update_job(job)
        
        logger.info(f"Added scene {scene.id} to job {scene.job_id}")
        return scene
    
    def get_scene(self, scene_id: str) -> Optional[Scene]:
        """Get scene by ID"""
        return self._scenes.get(scene_id)
    
    def update_scene(self, scene: Scene) -> Scene:
        """Update scene"""
        scene.updated_at = datetime.utcnow()
        self._scenes[scene.id] = scene
        return scene
    
    def add_shot(self, shot: Shot) -> Shot:
        """Add a shot to storage"""
        self._shots[shot.id] = shot
        
        # Update scene's shots list
        scene = self.get_scene(shot.scene_id)
        if scene:
            if shot not in scene.shots:
                scene.shots.append(shot)
                self.update_scene(scene)
        
        logger.info(f"Added shot {shot.id} to scene {shot.scene_id}")
        return shot
    
    def get_shot(self, shot_id: str) -> Optional[Shot]:
        """Get shot by ID"""
        return self._shots.get(shot_id)
    
    def update_shot(self, shot: Shot) -> Shot:
        """Update shot"""
        shot.updated_at = datetime.utcnow()
        self._shots[shot.id] = shot
        return shot
    
    def get_job_scenes(self, job_id: str) -> List[Scene]:
        """Get all scenes for a job"""
        return [s for s in self._scenes.values() if s.job_id == job_id]
    
    def get_scene_shots(self, scene_id: str) -> List[Shot]:
        """Get all shots for a scene"""
        return [s for s in self._shots.values() if s.scene_id == scene_id]
    
    def clear(self) -> None:
        """Clear all storage (for testing)"""
        self._jobs.clear()
        self._scenes.clear()
        self._shots.clear()


# Global store instance
_job_store = JobStore()


def get_job_store() -> JobStore:
    """Get the global job store instance"""
    return _job_store

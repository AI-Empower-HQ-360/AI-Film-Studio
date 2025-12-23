"""
Cost governance service for budget management.
"""
from datetime import datetime, timedelta
from typing import Optional


class CostGovernance:
    """
    Cost governance system to manage and track spending.
    """
    
    # Cost estimates for different services (in USD)
    SERVICE_COSTS = {
        "image_generation": 0.02,      # per image
        "video_generation": 0.50,       # per second
        "voice_synthesis": 0.015,       # per second
        "music_synthesis": 0.01,        # per second
        "ffmpeg_processing": 0.001,     # per second
        "storage": 0.023,               # per GB per month
    }
    
    def __init__(
        self,
        max_cost_per_job: float = 100.0,
        max_cost_per_user_daily: float = 500.0
    ):
        """
        Initialize cost governance.
        
        Args:
            max_cost_per_job: Maximum cost allowed per job
            max_cost_per_user_daily: Maximum cost per user per day
        """
        self.max_cost_per_job = max_cost_per_job
        self.max_cost_per_user_daily = max_cost_per_user_daily
    
    def estimate_job_cost(self, job_config: dict) -> dict:
        """
        Estimate cost for a job based on configuration.
        
        Args:
            job_config: Job configuration with task details
        
        Returns:
            dict: Cost breakdown and total estimate
        """
        breakdown = {}
        total_cost = 0.0
        
        # Image generation cost
        num_images = job_config.get("num_images", 10)
        image_cost = num_images * self.SERVICE_COSTS["image_generation"]
        breakdown["image_generation"] = image_cost
        total_cost += image_cost
        
        # Video generation cost
        video_duration = job_config.get("video_duration", 30)  # seconds
        video_cost = video_duration * self.SERVICE_COSTS["video_generation"]
        breakdown["video_generation"] = video_cost
        total_cost += video_cost
        
        # Voice synthesis cost
        if job_config.get("include_voice", True):
            voice_duration = job_config.get("voice_duration", video_duration)
            voice_cost = voice_duration * self.SERVICE_COSTS["voice_synthesis"]
            breakdown["voice_synthesis"] = voice_cost
            total_cost += voice_cost
        
        # Music synthesis cost
        if job_config.get("include_music", True):
            music_duration = job_config.get("music_duration", video_duration)
            music_cost = music_duration * self.SERVICE_COSTS["music_synthesis"]
            breakdown["music_synthesis"] = music_cost
            total_cost += music_cost
        
        # FFmpeg processing cost
        processing_cost = video_duration * self.SERVICE_COSTS["ffmpeg_processing"]
        breakdown["ffmpeg_processing"] = processing_cost
        total_cost += processing_cost
        
        return {
            "breakdown": breakdown,
            "total": round(total_cost, 2),
            "currency": "USD"
        }
    
    def check_job_cost_limit(self, estimated_cost: float) -> tuple[bool, Optional[str]]:
        """
        Check if job cost is within limits.
        
        Args:
            estimated_cost: Estimated cost for the job
        
        Returns:
            tuple: (is_allowed, reason)
        """
        if estimated_cost > self.max_cost_per_job:
            return False, f"Job cost ${estimated_cost:.2f} exceeds limit ${self.max_cost_per_job:.2f}"
        return True, None
    
    def check_user_daily_limit(
        self,
        user_id: int,
        new_cost: float,
        existing_daily_cost: float
    ) -> tuple[bool, Optional[str]]:
        """
        Check if user's daily cost limit would be exceeded.
        
        Args:
            user_id: User ID
            new_cost: Cost of new job
            existing_daily_cost: User's existing cost for today
        
        Returns:
            tuple: (is_allowed, reason)
        """
        total_cost = existing_daily_cost + new_cost
        if total_cost > self.max_cost_per_user_daily:
            return False, (
                f"Daily cost ${total_cost:.2f} would exceed limit "
                f"${self.max_cost_per_user_daily:.2f}"
            )
        return True, None
    
    def record_actual_cost(
        self,
        service: str,
        usage: float
    ) -> float:
        """
        Calculate actual cost based on usage.
        
        Args:
            service: Service name
            usage: Usage amount (varies by service)
        
        Returns:
            float: Actual cost
        """
        unit_cost = self.SERVICE_COSTS.get(service, 0.0)
        return round(usage * unit_cost, 4)


# Global cost governance instance
cost_governance = CostGovernance()

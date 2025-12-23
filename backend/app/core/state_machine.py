from enum import Enum


class JobStatus(str, Enum):
    """Job state machine states"""
    PENDING = "pending"
    VALIDATING = "validating"
    QUEUED = "queued"
    PROCESSING = "processing"
    GENERATING_IMAGES = "generating_images"
    GENERATING_VIDEO = "generating_video"
    GENERATING_AUDIO = "generating_audio"
    COMPOSING = "composing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class JobTransitions:
    """Defines valid state transitions for jobs"""
    
    VALID_TRANSITIONS = {
        JobStatus.PENDING: [JobStatus.VALIDATING, JobStatus.FAILED, JobStatus.CANCELLED],
        JobStatus.VALIDATING: [JobStatus.QUEUED, JobStatus.FAILED, JobStatus.CANCELLED],
        JobStatus.QUEUED: [JobStatus.PROCESSING, JobStatus.FAILED, JobStatus.CANCELLED],
        JobStatus.PROCESSING: [
            JobStatus.GENERATING_IMAGES,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        ],
        JobStatus.GENERATING_IMAGES: [
            JobStatus.GENERATING_VIDEO,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        ],
        JobStatus.GENERATING_VIDEO: [
            JobStatus.GENERATING_AUDIO,
            JobStatus.COMPOSING,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        ],
        JobStatus.GENERATING_AUDIO: [
            JobStatus.COMPOSING,
            JobStatus.FAILED,
            JobStatus.CANCELLED,
        ],
        JobStatus.COMPOSING: [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED],
        JobStatus.COMPLETED: [],
        JobStatus.FAILED: [],
        JobStatus.CANCELLED: [],
    }
    
    @classmethod
    def can_transition(cls, from_status: JobStatus, to_status: JobStatus) -> bool:
        """Check if a status transition is valid"""
        return to_status in cls.VALID_TRANSITIONS.get(from_status, [])
    
    @classmethod
    def get_next_states(cls, current_status: JobStatus) -> list[JobStatus]:
        """Get all valid next states for a given status"""
        return cls.VALID_TRANSITIONS.get(current_status, [])

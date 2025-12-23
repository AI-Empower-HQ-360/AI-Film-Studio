"""
Job state machine implementation.
"""
from enum import Enum
from typing import Optional
from datetime import datetime


class JobState(str, Enum):
    """Valid job states."""
    PENDING = "pending"
    QUEUED = "queued"
    MODERATING = "moderating"
    MODERATION_FAILED = "moderation_failed"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


# State transition rules
STATE_TRANSITIONS = {
    JobState.PENDING: [JobState.QUEUED, JobState.CANCELLED],
    JobState.QUEUED: [JobState.MODERATING, JobState.CANCELLED],
    JobState.MODERATING: [JobState.PROCESSING, JobState.MODERATION_FAILED, JobState.CANCELLED],
    JobState.MODERATION_FAILED: [JobState.CANCELLED],
    JobState.PROCESSING: [JobState.COMPLETED, JobState.FAILED, JobState.CANCELLED],
    JobState.COMPLETED: [],
    JobState.FAILED: [JobState.QUEUED, JobState.CANCELLED],  # Allow retry
    JobState.CANCELLED: [],
}


class JobStateMachine:
    """State machine for job lifecycle management."""
    
    def __init__(self, current_state: str):
        """Initialize state machine with current state."""
        self.current_state = JobState(current_state)
    
    def can_transition_to(self, new_state: str) -> bool:
        """Check if transition to new state is valid."""
        try:
            target_state = JobState(new_state)
        except ValueError:
            return False
        
        return target_state in STATE_TRANSITIONS.get(self.current_state, [])
    
    def transition_to(self, new_state: str, reason: Optional[str] = None) -> dict:
        """
        Transition to a new state.
        
        Returns:
            dict: Transition information including from_state, to_state, reason, timestamp
        
        Raises:
            ValueError: If transition is not allowed
        """
        if not self.can_transition_to(new_state):
            raise ValueError(
                f"Invalid state transition from {self.current_state.value} to {new_state}. "
                f"Valid transitions: {[s.value for s in STATE_TRANSITIONS.get(self.current_state, [])]}"
            )
        
        transition_info = {
            "from_state": self.current_state.value,
            "to_state": new_state,
            "reason": reason,
            "timestamp": datetime.utcnow(),
        }
        
        self.current_state = JobState(new_state)
        return transition_info
    
    def get_available_transitions(self) -> list[str]:
        """Get list of valid next states."""
        return [state.value for state in STATE_TRANSITIONS.get(self.current_state, [])]
    
    @staticmethod
    def is_terminal_state(state: str) -> bool:
        """Check if state is terminal (no further transitions)."""
        try:
            job_state = JobState(state)
            return len(STATE_TRANSITIONS.get(job_state, [])) == 0
        except ValueError:
            return False

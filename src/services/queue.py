"""Queue management system for task distribution"""
from typing import Optional, List, Dict, Any
from collections import deque
from datetime import datetime
from src.models.workflow import TaskMessage, TaskStatus
from src.utils.logger import setup_logger

logger = setup_logger(__name__)


class TaskQueue:
    """In-memory task queue with retry and DLQ support"""
    
    def __init__(self):
        self._queue: deque = deque()
        self._processing: Dict[str, TaskMessage] = {}
        self._dlq: List[TaskMessage] = []
        self._completed: List[str] = []
        
    def enqueue(self, task: TaskMessage) -> None:
        """Add task to queue"""
        logger.info(f"Enqueuing task {task.id} for job {task.job_id}")
        self._queue.append(task)
        
    def enqueue_batch(self, tasks: List[TaskMessage]) -> None:
        """Add multiple tasks to queue"""
        for task in tasks:
            self.enqueue(task)
    
    def dequeue(self) -> Optional[TaskMessage]:
        """Get next task from queue"""
        if not self._queue:
            return None
        
        task = self._queue.popleft()
        self._processing[task.id] = task
        logger.info(f"Dequeued task {task.id} for job {task.job_id}")
        return task
    
    def complete_task(self, task_id: str) -> None:
        """Mark task as completed"""
        if task_id in self._processing:
            task = self._processing.pop(task_id)
            self._completed.append(task_id)
            logger.info(f"Task {task_id} completed successfully")
    
    def fail_task(self, task_id: str, error: str) -> bool:
        """
        Mark task as failed and handle retry logic
        Returns True if task was re-queued, False if moved to DLQ
        """
        if task_id not in self._processing:
            logger.warning(f"Task {task_id} not found in processing queue")
            return False
        
        task = self._processing.pop(task_id)
        task.retry_count += 1
        
        if task.retry_count <= task.max_retries:
            logger.warning(f"Task {task_id} failed, retrying ({task.retry_count}/{task.max_retries})")
            self.enqueue(task)
            return True
        else:
            logger.error(f"Task {task_id} failed after {task.max_retries} retries, moving to DLQ")
            self._dlq.append(task)
            return False
    
    def get_queue_depth(self) -> int:
        """Get number of pending tasks"""
        return len(self._queue)
    
    def get_processing_count(self) -> int:
        """Get number of tasks currently being processed"""
        return len(self._processing)
    
    def get_dlq_count(self) -> int:
        """Get number of tasks in dead-letter queue"""
        return len(self._dlq)
    
    def get_completed_count(self) -> int:
        """Get number of completed tasks"""
        return len(self._completed)
    
    def get_dlq_tasks(self) -> List[TaskMessage]:
        """Get all tasks in dead-letter queue"""
        return self._dlq.copy()
    
    def clear(self) -> None:
        """Clear all queues (for testing)"""
        self._queue.clear()
        self._processing.clear()
        self._dlq.clear()
        self._completed.clear()


# Global queue instance
_task_queue = TaskQueue()


def get_task_queue() -> TaskQueue:
    """Get the global task queue instance"""
    return _task_queue

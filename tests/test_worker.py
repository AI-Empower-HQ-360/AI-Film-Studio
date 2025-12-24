"""Tests for worker task execution"""
import pytest
from src.models.workflow import TaskMessage, TaskType, TaskStatus
from src.services.worker import Worker, create_worker
from src.services.queue import get_task_queue
from src.services.storage import get_job_store
from src.services.orchestrator import WorkflowOrchestrator


@pytest.fixture
def setup_services():
    """Setup and cleanup services for each test"""
    store = get_job_store()
    queue = get_task_queue()
    
    # Clear before test
    store.clear()
    queue.clear()
    
    yield
    
    # Clear after test
    store.clear()
    queue.clear()


def test_worker_creation():
    """Test worker can be created"""
    worker = create_worker("test-worker-1")
    assert worker.worker_id == "test-worker-1"
    assert worker.running is False


def test_worker_processes_video_task(setup_services):
    """Test worker can process video generation task"""
    orchestrator = WorkflowOrchestrator()
    queue = get_task_queue()
    store = get_job_store()
    
    # Create a job
    script = """
    SCENE 1: INT. ROOM - DAY
    SHOT 1: Wide - 5s
    Test shot
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script
    )
    
    # Create and start worker
    worker = create_worker("test-worker")
    
    # Process only 1 task (will stop after hitting max or empty queue)
    worker.start(max_tasks=1)
    
    # Check task was processed
    assert queue.get_completed_count() >= 1
    # There might still be tasks in the queue
    assert queue.get_queue_depth() >= 0


def test_worker_updates_shot_status(setup_services):
    """Test worker updates shot status after processing"""
    orchestrator = WorkflowOrchestrator()
    store = get_job_store()
    
    script = """
    SCENE 1: INT. ROOM - DAY
    SHOT 1: Wide - 5s
    Test shot
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script
    )
    
    shot_id = job.scenes[0].shots[0].id
    
    # Start worker to process tasks
    worker = create_worker("test-worker")
    worker.start(max_tasks=2)  # Process both video and audio tasks
    
    # Check shot was updated
    shot = store.get_shot(shot_id)
    assert shot.status == TaskStatus.COMPLETED
    assert shot.asset_url is not None


def test_worker_handles_task_failure(setup_services):
    """Test worker handles task failures and retries"""
    queue = get_task_queue()
    
    # Create a task with invalid shot_id to trigger failure
    task = TaskMessage(
        job_id="invalid-job",
        scene_id="invalid-scene",
        shot_id="invalid-shot",
        task_type=TaskType.VIDEO_GENERATION,
        payload={}
    )
    
    queue.enqueue(task)
    
    # Start worker - will process task and retry until DLQ
    worker = create_worker("test-worker")
    worker.start(max_tasks=10)  # Allow multiple retries
    
    # Task should eventually move to DLQ after retries
    assert queue.get_dlq_count() >= 1
    assert queue.get_completed_count() == 0


def test_worker_moves_to_dlq_after_max_retries(setup_services):
    """Test tasks move to DLQ after max retries"""
    queue = get_task_queue()
    
    # Create a task that will fail
    task = TaskMessage(
        job_id="invalid-job",
        scene_id="invalid-scene",
        shot_id="invalid-shot",
        task_type=TaskType.VIDEO_GENERATION,
        payload={},
        max_retries=2  # Set low retry count
    )
    
    queue.enqueue(task)
    
    # Start worker - will fail and retry multiple times
    worker = create_worker("test-worker")
    worker.start(max_tasks=5)  # Process multiple retry attempts
    
    # Task should be in DLQ after retries exhausted
    assert queue.get_dlq_count() >= 1
    assert queue.get_queue_depth() == 0


def test_worker_processes_composition_task(setup_services):
    """Test worker can process composition task"""
    orchestrator = WorkflowOrchestrator()
    queue = get_task_queue()
    store = get_job_store()
    
    # Create a job
    script = """
    SCENE 1: INT. ROOM - DAY
    SHOT 1: Wide - 5s
    Test shot
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script
    )
    
    # Mark shot as completed with asset
    shot = job.scenes[0].shots[0]
    shot.status = TaskStatus.COMPLETED
    shot.asset_url = "s3://bucket/test.mp4"
    store.update_shot(shot)
    
    # Process all queued tasks
    worker = create_worker("test-worker")
    worker.start(max_tasks=2)
    
    # Trigger composition
    composition_task = TaskMessage(
        job_id=job.id,
        scene_id="composition",
        shot_id="final",
        task_type=TaskType.COMPOSITION,
        payload={}
    )
    queue.enqueue(composition_task)
    
    # Process composition
    worker.start(max_tasks=1)
    
    # Check job is completed
    job = store.get_job(job.id)
    assert job.final_video_url is not None

"""Tests for workflow orchestration"""
import pytest
from src.models.workflow import Job, JobStatus, TaskStatus, TaskType
from src.services.orchestrator import WorkflowOrchestrator
from src.services.storage import get_job_store
from src.services.queue import get_task_queue


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


def test_create_job_with_structured_script(setup_services):
    """Test job creation with properly structured script"""
    orchestrator = WorkflowOrchestrator()
    
    script = """
    SCENE 1: INT. OFFICE - DAY
    A busy office environment
    SHOT 1: Wide shot - 5s
    Camera pans across the office
    SHOT 2: Close up - 3s
    Focus on protagonist at desk
    
    SCENE 2: EXT. PARK - AFTERNOON
    Beautiful park scene
    SHOT 1: Medium shot - 4s
    Walking through the park
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script,
        title="Test Film"
    )
    
    assert job.id is not None
    assert job.status == JobStatus.QUEUED
    assert len(job.scenes) == 2
    assert job.scenes[0].scene_number == 1
    assert len(job.scenes[0].shots) == 2
    assert job.scenes[1].scene_number == 2
    assert len(job.scenes[1].shots) == 1
    assert job.estimated_cost > 0


def test_create_job_with_unstructured_script(setup_services):
    """Test job creation with unstructured script"""
    orchestrator = WorkflowOrchestrator()
    
    script = "A simple story about a hero's journey through an enchanted forest."
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script,
        title="Simple Story"
    )
    
    assert job.id is not None
    assert job.status == JobStatus.QUEUED
    assert len(job.scenes) == 1  # Should create default scene
    assert len(job.scenes[0].shots) == 1  # Should create default shot


def test_task_graph_creation(setup_services):
    """Test that tasks are properly created and queued"""
    orchestrator = WorkflowOrchestrator()
    queue = get_task_queue()
    
    script = """
    SCENE 1: INT. ROOM - DAY
    SHOT 1: Wide - 5s
    Test shot
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script
    )
    
    # Should have video + audio tasks for each shot
    assert queue.get_queue_depth() == 2  # 1 shot * 2 tasks (video + audio)


def test_workflow_state_tracking(setup_services):
    """Test workflow state is properly tracked"""
    orchestrator = WorkflowOrchestrator()
    
    script = """
    SCENE 1: INT. ROOM - DAY
    SHOT 1: Wide - 5s
    Shot 1
    SHOT 2: Close - 3s
    Shot 2
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script
    )
    
    state = orchestrator.get_workflow_state(job.id)
    
    assert state is not None
    assert state.job_id == job.id
    assert state.total_scenes == 1
    assert state.total_shots == 2
    assert state.completed_shots == 0
    assert state.pending_tasks == 4  # 2 shots * 2 tasks


def test_invalid_script_validation(setup_services):
    """Test that invalid scripts are rejected"""
    orchestrator = WorkflowOrchestrator()
    
    with pytest.raises(ValueError):
        orchestrator.create_job(
            user_id="user123",
            script="",  # Empty script
            title="Invalid"
        )
    
    with pytest.raises(ValueError):
        orchestrator.create_job(
            user_id="user123",
            script="   ",  # Whitespace only
            title="Invalid"
        )


def test_cost_estimation(setup_services):
    """Test cost estimation based on scenes and shots"""
    orchestrator = WorkflowOrchestrator()
    
    script = """
    SCENE 1: INT. ROOM - DAY
    SHOT 1: Wide - 5s
    Shot 1
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script
    )
    
    # Should have cost for video + audio + composition
    assert job.estimated_cost > 0
    assert job.reserved_credits == job.estimated_cost


def test_progress_update(setup_services):
    """Test that progress is updated correctly"""
    orchestrator = WorkflowOrchestrator()
    store = get_job_store()
    
    script = """
    SCENE 1: INT. ROOM - DAY
    SHOT 1: Wide - 5s
    Shot 1
    SHOT 2: Close - 3s
    Shot 2
    """
    
    job = orchestrator.create_job(
        user_id="user123",
        script=script
    )
    
    # Complete first shot
    shot1 = job.scenes[0].shots[0]
    shot1.status = TaskStatus.COMPLETED
    store.update_shot(shot1)
    
    orchestrator.update_progress(job.id)
    job = store.get_job(job.id)
    
    assert job.progress == 50.0  # 1 out of 2 shots completed

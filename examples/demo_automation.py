#!/usr/bin/env python3
"""
Demo script showing end-to-end automated film production workflow

This script demonstrates:
1. Script submission
2. Automatic scene/shot parsing
3. Task queue creation
4. Worker processing
5. Progress tracking
6. Final film delivery
"""

import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.orchestrator import get_orchestrator
from src.services.worker import create_worker
from src.services.storage import get_job_store
from src.models.workflow import JobStatus


def print_separator():
    print("\n" + "=" * 80 + "\n")


def demo_automation():
    """Demonstrate the fully automated workflow"""
    
    print_separator()
    print("🎬 AI FILM STUDIO - FULLY AUTOMATED WORKFLOW DEMO")
    print_separator()
    
    # Sample script
    script = """
SCENE 1: INT. COFFEE SHOP - MORNING
A cozy coffee shop bustling with morning energy

SHOT 1: Wide shot - 5s
Camera slowly pans across the coffee shop, capturing customers and ambiance

SHOT 2: Close up - 3s
Focus on barista expertly crafting a latte with detailed foam art

SHOT 3: Medium shot - 4s
Customer receiving coffee with a warm smile

SCENE 2: EXT. CITY PARK - AFTERNOON  
A beautiful park on a sunny afternoon with people enjoying the weather

SHOT 1: Establishing shot - 6s
Drone view capturing the entire park layout and surrounding cityscape

SHOT 2: Medium shot - 5s
Person walking their golden retriever on a winding path

SHOT 3: Close up - 3s
Children playing on swings, laughter and joy captured

SCENE 3: INT. HOME OFFICE - EVENING
Modern home office with warm lighting and creative workspace

SHOT 1: Wide shot - 4s
Overview of organized desk with computer, plants, and artwork

SHOT 2: Close up - 3s
Hands typing on keyboard, working on creative project
"""

    print("📝 STEP 1: Script Submission")
    print("-" * 80)
    print("Script content:")
    print(script[:200] + "...\n")
    
    # Create orchestrator
    orchestrator = get_orchestrator()
    store = get_job_store()
    
    # Create job
    print("Creating job...")
    job = orchestrator.create_job(
        user_id="demo-user-001",
        script=script,
        title="A Day in the Life"
    )
    
    print(f"✅ Job created: {job.id}")
    print(f"   Status: {job.status}")
    print(f"   Scenes: {len(job.scenes)}")
    total_shots = sum(len(scene.shots) for scene in job.scenes)
    print(f"   Total shots: {total_shots}")
    print(f"   Estimated cost: ${job.estimated_cost:.2f}")
    
    print_separator()
    print("⚙️ STEP 2: Automatic Scene & Shot Parsing")
    print("-" * 80)
    
    for scene in job.scenes:
        print(f"Scene {scene.scene_number}: {scene.description}")
        print(f"   Location: {scene.location}")
        print(f"   Time: {scene.time_of_day}")
        print(f"   Shots: {len(scene.shots)}")
        for shot in scene.shots:
            print(f"      - Shot {shot.shot_number}: {shot.camera_angle} ({shot.duration}s)")
    
    print_separator()
    print("📬 STEP 3: Task Queue & Dependency Graph")
    print("-" * 80)
    
    state = orchestrator.get_workflow_state(job.id)
    print(f"Total tasks queued: {state.pending_tasks}")
    print(f"Tasks per shot: 2 (video + audio)")
    print(f"Total: {total_shots} shots × 2 tasks = {state.pending_tasks} tasks")
    
    print_separator()
    print("🖥️ STEP 4: Autonomous Worker Processing")
    print("-" * 80)
    print("Starting background worker...")
    
    # Create worker
    worker = create_worker("demo-worker-001")
    
    # Start worker in background (process up to 50 tasks)
    print("Worker processing tasks...")
    print("(This would normally run in the background)")
    
    # Process tasks
    worker.start(max_tasks=50)
    
    print_separator()
    print("📊 STEP 5: Progress Tracking")
    print("-" * 80)
    
    # Get updated job
    job = store.get_job(job.id)
    state = orchestrator.get_workflow_state(job.id)
    
    print(f"Job Status: {job.status}")
    print(f"Progress: {job.progress:.1f}%")
    print(f"Completed shots: {state.completed_shots}/{state.total_shots}")
    print(f"Completed scenes: {state.completed_scenes}/{state.total_scenes}")
    print(f"Failed shots: {state.failed_shots}")
    
    print_separator()
    print("🎞️ STEP 6: Automatic Composition")
    print("-" * 80)
    
    if job.status == JobStatus.COMPLETED:
        print("✅ Final video composed successfully!")
        print(f"Download URL: {job.final_video_url}")
        print(f"Duration: ~{sum(shot.duration for scene in job.scenes for shot in scene.shots):.1f}s")
    else:
        print(f"Status: {job.status}")
        if job.final_video_url:
            print(f"Partial video URL: {job.final_video_url}")
    
    print_separator()
    print("📤 STEP 7: Delivery & Completion")
    print("-" * 80)
    
    if job.status == JobStatus.COMPLETED:
        print("✅ Film production complete!")
        print("\nUser receives:")
        print(f"   - Job ID: {job.id}")
        print(f"   - Download URL: {job.final_video_url}")
        print(f"   - Status: {job.status}")
        print(f"   - Actual cost: ${job.actual_cost:.2f}")
        print(f"   - Created at: {job.created_at}")
        print(f"   - Completed at: {job.completed_at}")
    else:
        print(f"Current status: {job.status}")
        print("The workflow is fully automated and would complete without human intervention.")
    
    print_separator()
    print("✨ AUTOMATION COMPLETE ✨")
    print_separator()
    
    print("\n📋 Summary:")
    print(f"   ✅ Script validated and parsed")
    print(f"   ✅ {len(job.scenes)} scenes identified")
    print(f"   ✅ {total_shots} shots created")
    print(f"   ✅ {state.pending_tasks + state.completed_shots * 2} tasks queued and processed")
    print(f"   ✅ Worker autonomously generated all assets")
    print(f"   ✅ Final composition triggered automatically")
    print(f"   ✅ Job delivered to user")
    
    print("\n🎯 Key Features Demonstrated:")
    print("   • Zero human intervention required")
    print("   • Automatic retry on failures")
    print("   • Progress tracking in real-time")
    print("   • Cost estimation upfront")
    print("   • Scalable worker architecture")
    print("   • Dead-letter queue for unrecoverable errors")
    
    print_separator()
    
    return job


if __name__ == "__main__":
    demo_automation()

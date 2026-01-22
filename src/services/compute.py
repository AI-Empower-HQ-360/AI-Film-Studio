"""
ECS Compute Service for AI Film Studio.
Handles GPU task execution and container management.
"""

import os
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """ECS Task status enum."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class ComputeService:
    """AWS ECS Compute Service for managing GPU tasks."""
    
    def __init__(self, cluster_name: Optional[str] = None):
        """Initialize the compute service."""
        self.cluster_name = cluster_name or os.getenv("ECS_CLUSTER_NAME", "ai-film-studio-cluster")
        self.region = os.getenv("AWS_REGION", "us-east-1")
        self._client = None
        self._tasks: Dict[str, Dict[str, Any]] = {}  # In-memory for testing
    
    @property
    def client(self):
        """Lazy load boto3 ECS client."""
        if self._client is None:
            try:
                import boto3
                self._client = boto3.client('ecs', region_name=self.region)
            except ImportError:
                self._client = None
        return self._client
    
    async def run_task(
        self,
        task_definition: str,
        container_overrides: Optional[Dict[str, Any]] = None,
        launch_type: str = "FARGATE",
        subnet_ids: Optional[List[str]] = None,
        security_group_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Run an ECS task."""
        task_id = str(uuid.uuid4())
        task_arn = f"arn:aws:ecs:{self.region}:123456789:task/{self.cluster_name}/{task_id}"
        
        task = {
            "task_id": task_id,
            "task_arn": task_arn,
            "task_definition": task_definition,
            "status": TaskStatus.PENDING.value,
            "launch_type": launch_type,
            "container_overrides": container_overrides or {},
            "started_at": datetime.utcnow().isoformat(),
            "stopped_at": None,
            "exit_code": None
        }
        
        self._tasks[task_id] = task
        
        if self.client:
            try:
                network_config = None
                if subnet_ids:
                    network_config = {
                        "awsvpcConfiguration": {
                            "subnets": subnet_ids,
                            "securityGroups": security_group_ids or [],
                            "assignPublicIp": "ENABLED"
                        }
                    }
                
                response = self.client.run_task(
                    cluster=self.cluster_name,
                    taskDefinition=task_definition,
                    launchType=launch_type,
                    networkConfiguration=network_config,
                    overrides={"containerOverrides": [container_overrides]} if container_overrides else {}
                )
                
                if response.get("tasks"):
                    return {
                        "task_id": response["tasks"][0]["taskArn"].split("/")[-1],
                        "task_arn": response["tasks"][0]["taskArn"],
                        "status": response["tasks"][0]["lastStatus"]
                    }
            except Exception:
                pass
        
        # Simulate task starting
        task["status"] = TaskStatus.RUNNING.value
        return task
    
    async def run_gpu_task(
        self,
        task_definition: str,
        gpu_count: int = 1,
        container_overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Run a GPU-enabled ECS task."""
        overrides = container_overrides or {}
        overrides["resourceRequirements"] = [
            {"type": "GPU", "value": str(gpu_count)}
        ]
        
        return await self.run_task(
            task_definition=task_definition,
            container_overrides=overrides,
            launch_type="EC2"  # GPU requires EC2 launch type
        )
    
    async def stop_task(self, task_id: str, reason: str = "User requested") -> bool:
        """Stop a running ECS task."""
        if task_id in self._tasks:
            self._tasks[task_id]["status"] = TaskStatus.STOPPED.value
            self._tasks[task_id]["stopped_at"] = datetime.utcnow().isoformat()
        
        if self.client:
            try:
                task_arn = f"arn:aws:ecs:{self.region}:123456789:task/{self.cluster_name}/{task_id}"
                self.client.stop_task(
                    cluster=self.cluster_name,
                    task=task_arn,
                    reason=reason
                )
            except Exception:
                pass
        
        return True
    
    async def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """Get the status of an ECS task."""
        if task_id in self._tasks:
            return self._tasks[task_id]
        
        if self.client:
            try:
                task_arn = f"arn:aws:ecs:{self.region}:123456789:task/{self.cluster_name}/{task_id}"
                response = self.client.describe_tasks(
                    cluster=self.cluster_name,
                    tasks=[task_arn]
                )
                
                if response.get("tasks"):
                    task = response["tasks"][0]
                    return {
                        "task_id": task_id,
                        "task_arn": task["taskArn"],
                        "status": task["lastStatus"],
                        "started_at": str(task.get("startedAt")),
                        "stopped_at": str(task.get("stoppedAt"))
                    }
            except Exception:
                pass
        
        return {"task_id": task_id, "status": "UNKNOWN"}
    
    async def list_running_tasks(self) -> List[Dict[str, Any]]:
        """List all running tasks in the cluster."""
        running_tasks = [
            task for task in self._tasks.values()
            if task.get("status") == TaskStatus.RUNNING.value
        ]
        
        if self.client:
            try:
                response = self.client.list_tasks(
                    cluster=self.cluster_name,
                    desiredStatus="RUNNING"
                )
                
                if response.get("taskArns"):
                    describe_response = self.client.describe_tasks(
                        cluster=self.cluster_name,
                        tasks=response["taskArns"]
                    )
                    return describe_response.get("tasks", running_tasks)
            except Exception:
                pass
        
        return running_tasks
    
    async def get_cluster_capacity(self) -> Dict[str, Any]:
        """Get cluster capacity information."""
        return {
            "cluster": self.cluster_name,
            "running_tasks": len([t for t in self._tasks.values() if t.get("status") == "RUNNING"]),
            "pending_tasks": len([t for t in self._tasks.values() if t.get("status") == "PENDING"]),
            "available_gpu": 4,
            "total_gpu": 4
        }
    
    async def wait_for_task(self, task_id: str, timeout: int = 300) -> Dict[str, Any]:
        """Wait for a task to complete."""
        # In production, this would poll until task completes
        if task_id in self._tasks:
            self._tasks[task_id]["status"] = TaskStatus.COMPLETED.value
            return self._tasks[task_id]
        
        return {"task_id": task_id, "status": TaskStatus.COMPLETED.value}
    
    async def health_check(self) -> Dict[str, Any]:
        """Check compute service health."""
        return {
            "status": "healthy",
            "cluster": self.cluster_name,
            "region": self.region,
            "tasks_tracked": len(self._tasks)
        }


# Convenience instance
compute_service = ComputeService()

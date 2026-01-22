"""
ECS Compute Service
Handles ECS task operations for GPU workloads
"""
import os
import asyncio
import logging
from typing import Optional, Dict, Any, List

try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False
    ClientError = Exception

logger = logging.getLogger(__name__)


class ECSService:
    """Service for ECS task operations"""
    
    def __init__(self, region: str = "us-east-1"):
        """
        Initialize ECS service
        
        Args:
            region: AWS region
        """
        self.region = region
        if HAS_BOTO3:
            self.client = boto3.client("ecs", region_name=region)
        else:
            self.client = None
    
    async def run_gpu_task(
        self,
        task_definition: str,
        cluster: str,
        environment: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Run GPU-enabled ECS task
        
        Args:
            task_definition: ECS task definition name or ARN
            cluster: ECS cluster name
            environment: Environment variables dictionary
            **kwargs: Additional task parameters
            
        Returns:
            Task run response
        """
        if not self.client:
            raise ValueError("ECS client not initialized")
        
        try:
            # Prepare environment variables
            env_vars = []
            if environment:
                for key, value in environment.items():
                    env_vars.append({
                        "name": key,
                        "value": str(value)
                    })
            
            # Prepare overrides
            overrides = {}
            if env_vars:
                overrides["containerOverrides"] = [{
                    "name": kwargs.get("container_name", "app"),
                    "environment": env_vars
                }]
            
            response = self.client.run_task(
                cluster=cluster,
                taskDefinition=task_definition,
                overrides=overrides if overrides else None,
                **kwargs
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error running ECS task: {str(e)}")
            raise
    
    async def get_task_status(
        self,
        cluster: str,
        task_arn: str,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Get task status
        
        Args:
            cluster: ECS cluster name
            task_arn: Task ARN
            **kwargs: Additional parameters
            
        Returns:
            Task status dictionary
        """
        if not self.client:
            raise ValueError("ECS client not initialized")
        
        try:
            response = self.client.describe_tasks(
                cluster=cluster,
                tasks=[task_arn],
                **kwargs
            )
            
            if response.get("tasks"):
                task = response["tasks"][0]
                return {
                    "taskArn": task.get("taskArn"),
                    "lastStatus": task.get("lastStatus"),
                    "desiredStatus": task.get("desiredStatus"),
                    "containers": task.get("containers", []),
                    "startedAt": task.get("startedAt"),
                    "stoppedAt": task.get("stoppedAt")
                }
            
            return {}
            
        except Exception as e:
            logger.error(f"Error getting task status: {str(e)}")
            raise
    
    async def stop_task(
        self,
        cluster: str,
        task_arn: str,
        reason: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Stop running task
        
        Args:
            cluster: ECS cluster name
            task_arn: Task ARN
            reason: Optional stop reason
            **kwargs: Additional parameters
            
        Returns:
            Stop task response
        """
        if not self.client:
            raise ValueError("ECS client not initialized")
        
        try:
            response = self.client.stop_task(
                cluster=cluster,
                task=task_arn,
                reason=reason or "User requested stop",
                **kwargs
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Error stopping task: {str(e)}")
            raise
    
    async def list_tasks(
        self,
        cluster: str,
        status: Optional[str] = None,
        **kwargs
    ) -> List[str]:
        """
        List tasks in cluster
        
        Args:
            cluster: ECS cluster name
            status: Optional task status filter (RUNNING, STOPPED, etc.)
            **kwargs: Additional parameters
            
        Returns:
            List of task ARNs
        """
        if not self.client:
            raise ValueError("ECS client not initialized")
        
        try:
            params = {"cluster": cluster}
            if status:
                params["desiredStatus"] = status
            
            response = self.client.list_tasks(**params, **kwargs)
            
            return response.get("taskArns", [])
            
        except Exception as e:
            logger.error(f"Error listing tasks: {str(e)}")
            raise

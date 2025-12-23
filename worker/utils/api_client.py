import httpx
from typing import Optional
from config import settings


class APIClient:
    """Client for communicating with the backend API"""
    
    def __init__(self):
        self.base_url = settings.BACKEND_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: Optional[int] = None,
        error_message: Optional[str] = None,
        auth_token: Optional[str] = None
    ):
        """Update job status via API"""
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        payload = {"status": status}
        if progress is not None:
            payload["progress"] = progress
        if error_message:
            payload["error_message"] = error_message
        
        url = f"{self.base_url}/jobs/{job_id}/status"
        
        try:
            response = await self.client.patch(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error updating job status: {e}")
            return None
    
    async def get_job(self, job_id: str, auth_token: Optional[str] = None):
        """Get job details"""
        headers = {}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
        
        url = f"{self.base_url}/jobs/{job_id}"
        
        try:
            response = await self.client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting job: {e}")
            return None
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()


api_client = APIClient()

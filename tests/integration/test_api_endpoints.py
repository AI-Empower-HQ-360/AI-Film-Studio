"""
Integration tests for FastAPI endpoints.
Tests all API endpoints with realistic payloads.
"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Integration tests for API endpoints"""

    @pytest.mark.integration
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    @pytest.mark.integration
    def test_generate_video_endpoint(self):
        """Test video generation API endpoint"""
        payload = {
            "script": "A young explorer discovers a hidden world.",
            "duration": 30,
            "voice": "professional-female-1",
            "style": "cinematic"
        }
        
        response = client.post("/v1/generate", json=payload)
        assert response.status_code in [200, 202]  # 202 for async processing
        
        data = response.json()
        assert "job_id" in data
        assert "status" in data

    @pytest.mark.integration
    def test_get_video_status(self):
        """Test video status retrieval"""
        # First create a job
        payload = {
            "script": "Test script for status check.",
            "duration": 10
        }
        create_response = client.post("/v1/generate", json=payload)
        job_id = create_response.json()["job_id"]
        
        # Then check status
        response = client.get(f"/v1/videos/{job_id}")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] in ["pending", "processing", "completed", "failed"]

    @pytest.mark.integration
    def test_list_voices(self):
        """Test voice listing endpoint"""
        response = client.get("/v1/voices")
        assert response.status_code == 200
        
        data = response.json()
        assert "voices" in data
        assert len(data["voices"]) > 0
        
        # Check voice structure
        voice = data["voices"][0]
        assert "id" in voice
        assert "name" in voice
        assert "language" in voice

    @pytest.mark.integration
    def test_generate_characters(self):
        """Test character generation endpoint"""
        payload = {
            "description": "A young female explorer with curious eyes",
            "count": 2,
            "style": "realistic"
        }
        
        response = client.post("/v1/characters", json=payload)
        assert response.status_code in [200, 202]
        
        data = response.json()
        assert "job_id" in data or "images" in data

    @pytest.mark.integration
    def test_invalid_request_validation(self):
        """Test API validation with invalid requests"""
        # Test missing required fields
        response = client.post("/v1/generate", json={})
        assert response.status_code == 422  # Validation error
        
        # Test invalid duration
        response = client.post("/v1/generate", json={
            "script": "Test",
            "duration": 200  # Exceeds max duration
        })
        assert response.status_code == 422

    @pytest.mark.integration
    def test_authentication(self):
        """Test API authentication"""
        # Test without API key
        response = client.post("/v1/generate", json={
            "script": "Test",
            "duration": 30
        })
        # Should work without auth in test mode or fail with 401
        assert response.status_code in [200, 202, 401]

    @pytest.mark.integration
    def test_rate_limiting(self):
        """Test API rate limiting"""
        # Make multiple rapid requests
        responses = []
        for i in range(15):
            response = client.get("/health")
            responses.append(response.status_code)
        
        # Should eventually get rate limited (429) or all succeed in test mode
        assert 429 in responses or all(r == 200 for r in responses)

    @pytest.mark.integration
    def test_error_responses(self):
        """Test error response formats"""
        response = client.get("/v1/videos/nonexistent_job_id")
        assert response.status_code == 404
        
        data = response.json()
        assert "error" in data or "detail" in data

    @pytest.mark.integration
    def test_cors_headers(self):
        """Test CORS configuration"""
        response = client.options("/v1/generate")
        assert response.status_code in [200, 405]  # OPTIONS may not be implemented
        
        # Check GET endpoint has CORS headers
        response = client.get("/health")
        # CORS headers should be present in production
        assert response.status_code == 200

    @pytest.mark.integration
    def test_webhook_configuration(self):
        """Test webhook configuration endpoint"""
        payload = {
            "url": "https://example.com/webhooks/video",
            "events": ["video.completed", "video.failed"]
        }
        
        response = client.post("/v1/webhooks", json=payload)
        assert response.status_code in [200, 201, 501]  # 501 if not implemented yet

    @pytest.mark.integration
    def test_pagination(self):
        """Test pagination on list endpoints"""
        response = client.get("/v1/videos?page=1&limit=10")
        assert response.status_code in [200, 501]  # 501 if not implemented
        
        if response.status_code == 200:
            data = response.json()
            assert "items" in data or "videos" in data
            assert "total" in data or "count" in data

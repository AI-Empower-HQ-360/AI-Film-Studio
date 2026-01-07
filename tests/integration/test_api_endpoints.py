"""Integration tests for API endpoints"""

import concurrent.futures

import pytest


@pytest.mark.integration
class TestAPIEndpoints:
    """Tests for FastAPI endpoints"""

    def test_root_endpoint(self, api_client):
        """Test root endpoint returns correct response"""
        response = api_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "status" in data
        assert data["status"] == "healthy"
        assert "AI Film Studio" in data["message"]

    def test_health_check_endpoint(self, api_client):
        """Test health check endpoint"""
        response = api_client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"
        assert data["service"] == "AI Film Studio"

    def test_health_check_response_format(self, api_client):
        """Test health check response has correct format"""
        response = api_client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()

        # Check all required fields are present
        required_fields = ["status", "version", "service"]
        for field in required_fields:
            assert field in data

    def test_invalid_endpoint_returns_404(self, api_client):
        """Test invalid endpoint returns 404"""
        response = api_client.get("/invalid/endpoint")

        assert response.status_code == 404

    def test_root_endpoint_response_type(self, api_client):
        """Test root endpoint returns JSON"""
        response = api_client.get("/")

        assert response.headers["content-type"] == "application/json"

    def test_health_endpoint_response_type(self, api_client):
        """Test health endpoint returns JSON"""
        response = api_client.get("/api/v1/health")

        assert response.headers["content-type"] == "application/json"

    @pytest.mark.asyncio
    async def test_async_root_endpoint(self, async_api_client):
        """Test root endpoint with async client"""
        response = await async_api_client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @pytest.mark.asyncio
    async def test_async_health_check(self, async_api_client):
        """Test health check with async client"""
        response = await async_api_client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["version"] == "0.1.0"

    def test_api_accepts_get_method_only_on_root(self, api_client):
        """Test root endpoint only accepts GET method"""
        # GET should work
        response = api_client.get("/")
        assert response.status_code == 200

        # POST should not be allowed
        response = api_client.post("/")
        assert response.status_code == 405  # Method Not Allowed

    def test_multiple_health_check_calls(self, api_client):
        """Test multiple health check calls return consistent results"""
        responses = []
        for _ in range(5):
            response = api_client.get("/api/v1/health")
            responses.append(response.json())

        # All responses should be identical
        first = responses[0]
        for response in responses[1:]:
            assert response == first

    def test_concurrent_requests(self, api_client):
        """Test API handles concurrent requests"""

        def make_request():
            return api_client.get("/api/v1/health")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            responses = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        assert len(responses) == 20
        for response in responses:
            assert response.status_code == 200

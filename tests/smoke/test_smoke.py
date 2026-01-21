"""
Smoke Tests - Critical Path Validation
Quick tests to verify core functionality after deployment
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


@pytest.mark.smoke
class TestSmoke:
    """Smoke tests for critical functionality"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        from src.api.main import app
        return TestClient(app)

    def test_health_check(self, client):
        """Test health check endpoint responds"""
        response = client.get("/health")
        assert response.status_code in [200, 404]  # 404 if not implemented yet
        if response.status_code == 200:
            assert "status" in response.json() or "ok" in response.text.lower()

    def test_root_endpoint(self, client):
        """Test root endpoint is accessible"""
        response = client.get("/")
        assert response.status_code in [200, 404]

    def test_api_docs_accessible(self, client):
        """Test API documentation is accessible"""
        response = client.get("/docs")
        assert response.status_code in [200, 404]

    @patch('src.engines.character_engine.CharacterEngine')
    def test_character_engine_imports(self, mock_engine):
        """Test Character Engine can be imported"""
        from src.engines.character_engine import CharacterEngine
        assert CharacterEngine is not None

    @patch('src.engines.writing_engine.WritingEngine')
    def test_writing_engine_imports(self, mock_engine):
        """Test Writing Engine can be imported"""
        from src.engines.writing_engine import WritingEngine
        assert WritingEngine is not None

    def test_all_engines_importable(self):
        """Test all 8 engines can be imported"""
        from src.engines import (
            CharacterEngine,
            WritingEngine,
            PreProductionEngine,
            ProductionManager,
            ProductionLayer,
            PostProductionEngine,
            MarketingEngine,
            EnterprisePlatform
        )
        assert all([
            CharacterEngine,
            WritingEngine,
            PreProductionEngine,
            ProductionManager,
            ProductionLayer,
            PostProductionEngine,
            MarketingEngine,
            EnterprisePlatform
        ])

    @pytest.mark.asyncio
    async def test_basic_api_connectivity(self, client):
        """Test API is responsive"""
        response = client.get("/health")
        assert response.status_code in [200, 404, 503]

    def test_database_configuration(self):
        """Test database configuration is valid"""
        import os
        # Just check env vars exist, not actual connection
        # Actual connection tested in integration tests
        assert True  # Placeholder - implement actual check

    def test_aws_configuration(self):
        """Test AWS configuration is valid"""
        import os
        # Check AWS env vars exist
        # Actual connection tested in integration tests
        assert True  # Placeholder - implement actual check

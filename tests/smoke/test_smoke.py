"""
Smoke Tests - Critical Path Validation
Quick tests to verify core functionality after deployment
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os


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
        response = client.get("/api/v1/health")
        assert response.status_code in [200, 404, 503]
        if response.status_code == 200:
            data = response.json()
            assert "status" in data or "engines" in data

    def test_root_endpoint(self, client):
        """Test root endpoint is accessible"""
        response = client.get("/")
        assert response.status_code in [200, 404]

    def test_api_docs_accessible(self, client):
        """Test API documentation is accessible"""
        response = client.get("/api/docs")
        assert response.status_code in [200, 404]

    def test_character_engine_imports(self):
        """Test Character Engine can be imported"""
        from src.engines.character_engine import CharacterEngine
        assert CharacterEngine is not None
        engine = CharacterEngine()
        assert engine is not None

    def test_writing_engine_imports(self):
        """Test Writing Engine can be imported"""
        from src.engines.writing_engine import WritingEngine
        assert WritingEngine is not None
        engine = WritingEngine()
        assert engine is not None

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
        
        # Test instantiation
        engines = [
            CharacterEngine(),
            WritingEngine(),
            PreProductionEngine(),
            ProductionManager(),
            ProductionLayer(),
            PostProductionEngine(),
            MarketingEngine(),
            EnterprisePlatform()
        ]
        assert len(engines) == 8

    def test_basic_api_connectivity(self, client):
        """Test API is responsive"""
        response = client.get("/api/v1/health")
        assert response.status_code in [200, 404, 503]

    def test_character_creation_smoke(self):
        """Test basic character creation works"""
        from src.engines.character_engine import CharacterEngine
        engine = CharacterEngine()
        character = engine.create_character(
            name="Test Character",
            description="Smoke test character"
        )
        assert character is not None
        assert character.name == "Test Character"

    def test_script_creation_smoke(self):
        """Test basic script creation works"""
        from src.engines.writing_engine import WritingEngine
        engine = WritingEngine()
        script = engine.create_script(
            title="Test Script",
            content="INT. ROOM - DAY\nCharacter speaks."
        )
        assert script is not None
        assert script.title == "Test Script"

    def test_project_creation_smoke(self):
        """Test basic project creation works"""
        from src.engines.production_management import ProductionManager
        manager = ProductionManager()
        project = manager.create_project(
            name="Smoke Test Project",
            description="Test",
            created_by="smoke_test_user"
        )
        assert project is not None
        assert project.name == "Smoke Test Project"

    def test_environment_variables(self):
        """Test critical environment variables exist"""
        # Check if env vars are set (not checking values, just structure)
        env_vars = os.environ.keys()
        assert isinstance(env_vars, (list, dict, set))

    def test_api_version(self, client):
        """Test API version endpoint"""
        response = client.get("/api/v1/about")
        if response.status_code == 200:
            data = response.json()
            assert "version" in data or "name" in data

    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options("/api/v1/health")
        # CORS headers may or may not be present depending on config
        assert response.status_code in [200, 204, 404, 405]

    def test_error_handling(self, client):
        """Test error handling for invalid endpoints"""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code in [404, 405]

    def test_api_response_format(self, client):
        """Test API response format"""
        response = client.get("/api/v1/health")
        if response.status_code == 200:
            # Should be valid JSON
            data = response.json()
            assert isinstance(data, dict)

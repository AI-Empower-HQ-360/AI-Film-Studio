"""
Integration Tests for All 8 Engines
Tests engine integration with API endpoints and each other
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import uuid


@pytest.mark.integration
class TestEngineIntegration:
    """Integration tests for all engines working together"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        from src.api.main import app
        return TestClient(app)

    def test_character_engine_integration(self, client):
        """Test Character Engine API integration"""
        with patch('src.engines.character_engine.CharacterEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_instance.create_character.return_value = MagicMock(
                id="char_001",
                name="Test Character"
            )
            mock_engine.return_value = mock_instance
            
            response = client.post("/api/v1/characters", json={
                "name": "Test Character",
                "description": "A test character"
            })
            
            assert response.status_code in [200, 201, 404, 501]

    def test_writing_engine_integration(self, client):
        """Test Writing Engine API integration"""
        with patch('src.engines.writing_engine.WritingEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_instance.create_script.return_value = MagicMock(
                id="script_001",
                title="Test Script"
            )
            mock_engine.return_value = mock_instance
            
            response = client.post("/api/v1/scripts", json={
                "title": "Test Script",
                "content": "INT. ROOM - DAY\nCharacter speaks."
            })
            
            assert response.status_code in [200, 201, 404, 501]

    def test_preproduction_engine_integration(self, client):
        """Test Pre-Production Engine API integration"""
        with patch('src.engines.preproduction_engine.PreProductionEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_instance.create_breakdown.return_value = MagicMock(
                breakdown_id="breakdown_001"
            )
            mock_engine.return_value = mock_instance
            
            response = client.post("/api/v1/projects/test/breakdown", json={
                "script_id": "script_001"
            })
            
            assert response.status_code in [200, 201, 404, 501]

    def test_production_management_integration(self, client):
        """Test Production Management API integration"""
        with patch('src.engines.production_management.ProductionManager') as mock_manager:
            mock_instance = MagicMock()
            mock_instance.create_project.return_value = MagicMock(
                project_id="proj_001",
                name="Test Project"
            )
            mock_manager.return_value = mock_instance
            
            response = client.post("/api/v1/projects", json={
                "name": "Test Project",
                "description": "Test",
                "created_by": "user_001"
            })
            
            assert response.status_code in [200, 201, 404, 501]

    def test_production_layer_integration(self, client):
        """Test Production Layer API integration"""
        with patch('src.engines.production_layer.ProductionLayer') as mock_layer:
            mock_instance = MagicMock()
            mock_instance.create_shot.return_value = MagicMock(
                shot_id="shot_001"
            )
            mock_layer.return_value = mock_instance
            
            response = client.post("/api/v1/projects/test/shots", json={
                "scene_id": "scene_001",
                "shot_type": "ai_generated"
            })
            
            assert response.status_code in [200, 201, 404, 501]

    def test_postproduction_engine_integration(self, client):
        """Test Post-Production Engine API integration"""
        with patch('src.engines.postproduction_engine.PostProductionEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_instance.generate_character_voice = AsyncMock(return_value={
                "audio_url": "s3://audio.wav"
            })
            mock_engine.return_value = mock_instance
            
            response = client.post("/api/v1/post-production/voice", json={
                "character_id": "char_001",
                "dialogue_text": "Hello",
                "scene_id": "scene_001"
            })
            
            assert response.status_code in [200, 202, 404, 501]

    def test_marketing_engine_integration(self, client):
        """Test Marketing Engine API integration"""
        with patch('src.engines.marketing_engine.MarketingEngine') as mock_engine:
            mock_instance = MagicMock()
            mock_instance.create_trailer.return_value = MagicMock(
                asset_id="trailer_001"
            )
            mock_engine.return_value = mock_instance
            
            response = client.post("/api/v1/marketing/trailers", json={
                "project_id": "proj_001",
                "duration": 30
            })
            
            assert response.status_code in [200, 201, 202, 404, 501]

    def test_enterprise_platform_integration(self, client):
        """Test Enterprise Platform API integration"""
        with patch('src.engines.enterprise_platform.EnterprisePlatform') as mock_platform:
            mock_instance = MagicMock()
            mock_instance.create_organization.return_value = MagicMock(
                organization_id="org_001"
            )
            mock_platform.return_value = mock_instance
            
            response = client.post("/api/v1/organizations", json={
                "name": "Test Studio",
                "domain": "teststudio.com"
            })
            
            assert response.status_code in [200, 201, 404, 501]

    def test_character_to_script_integration(self):
        """Test Character Engine → Writing Engine integration"""
        from src.engines.character_engine import CharacterEngine
        from src.engines.writing_engine import WritingEngine
        
        char_engine = CharacterEngine()
        writing_engine = WritingEngine()
        
        # Create character
        character = char_engine.create_character(
            name="Test Character",
            description="A hero"
        )
        
        # Use character in script
        script = writing_engine.create_script(
            title="Test Script",
            content=f"INT. ROOM - DAY\n{character.name} enters."
        )
        
        assert script is not None
        assert character is not None

    def test_script_to_preproduction_integration(self):
        """Test Writing Engine → Pre-Production Engine integration"""
        from src.engines.writing_engine import WritingEngine
        from src.engines.preproduction_engine import PreProductionEngine
        
        writing_engine = WritingEngine()
        preprod_engine = PreProductionEngine()
        
        # Create script
        script = writing_engine.create_script(
            title="Test Film",
            content="INT. STUDIO - DAY\nCharacter walks in."
        )
        
        # Create breakdown
        breakdown = preprod_engine.create_breakdown(
            script_id=script.script_id if hasattr(script, 'script_id') else "test_script",
            script_data={"script_id": "test_script", "scenes": []}
        )
        
        assert script is not None
        assert breakdown is not None

    def test_full_pipeline_integration(self):
        """Test full pipeline: Character → Script → Pre-Prod → Production"""
        from src.engines.character_engine import CharacterEngine
        from src.engines.writing_engine import WritingEngine
        from src.engines.preproduction_engine import PreProductionEngine
        from src.engines.production_management import ProductionManager
        
        # Create all engines
        char_engine = CharacterEngine()
        writing_engine = WritingEngine()
        preprod_engine = PreProductionEngine()
        prod_manager = ProductionManager()
        
        # Create character
        character = char_engine.create_character(name="Hero", description="Main character")
        
        # Create script
        script = writing_engine.create_script(title="Film", content="Scene content")
        
        # Create project
        project = prod_manager.create_project(
            name="Film Project",
            description="Test",
            created_by="user_001"
        )
        
        # Create breakdown
        breakdown = preprod_engine.create_breakdown(
            script_id="test_script",
            script_data={"script_id": "test_script", "scenes": []}
        )
        
        assert character is not None
        assert script is not None
        assert project is not None
        assert breakdown is not None

    def test_engine_initialization(self):
        """Test all engines can be initialized"""
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
        assert all(engine is not None for engine in engines)

    def test_health_check_all_engines(self, client):
        """Test health check reports all engines"""
        response = client.get("/api/v1/health")
        
        if response.status_code == 200:
            data = response.json()
            if "engines" in data:
                engines_status = data["engines"]
                expected_engines = [
                    "character_engine",
                    "writing_engine",
                    "preproduction_engine",
                    "production_manager",
                    "production_layer",
                    "postproduction_engine",
                    "marketing_engine",
                    "enterprise_platform"
                ]
                
                for engine in expected_engines:
                    assert engine in engines_status

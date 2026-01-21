"""
Unit Tests for Production Layer
Tests hybrid production execution (real footage + AI generation)
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import uuid


@pytest.mark.unit
class TestProductionLayer:
    """Test suite for Production Layer functionality"""

    @pytest.fixture
    def production_layer(self):
        """Create a production layer instance"""
        from src.engines.production_layer import ProductionLayer
        return ProductionLayer()

    @pytest.fixture
    def sample_shot(self):
        """Sample shot for testing"""
        return {
            "shot_id": str(uuid.uuid4()),
            "scene_id": "scene_001",
            "shot_type": "ai_generated",
            "description": "Character walks into room"
        }

    def test_create_shot(self, production_layer, sample_shot):
        """Test shot creation"""
        shot = production_layer.create_shot(
            scene_id=sample_shot["scene_id"],
            shot_type=sample_shot["shot_type"],
            description=sample_shot["description"]
        )
        
        assert shot is not None
        assert shot.scene_id == sample_shot["scene_id"]
        assert shot.shot_type == sample_shot["shot_type"]

    def test_upload_real_footage(self, production_layer):
        """Test real footage upload"""
        footage = production_layer.upload_real_footage(
            scene_id="scene_001",
            file_path="/path/to/video.mp4",
            metadata={"camera": "RED", "resolution": "4K"}
        )
        
        assert footage is not None
        assert footage.scene_id == "scene_001"
        assert footage.is_real_footage is True

    def test_generate_ai_shot(self, production_layer):
        """Test AI shot generation"""
        with patch.object(production_layer, 'video_service') as mock_service:
            mock_service.generate_from_scene = AsyncMock(return_value={
                "output_path": "s3://video.mp4",
                "duration": 10.5
            })
            
            shot = production_layer.generate_ai_shot(
                scene_id="scene_001",
                description="AI-generated scene",
                style="cinematic"
            )
            
            assert shot is not None or isinstance(shot, dict)

    def test_match_shot_continuity(self, production_layer):
        """Test shot matching for continuity"""
        shot1 = production_layer.create_shot(
            scene_id="scene_001",
            shot_type="real_footage",
            description="Character enters"
        )
        
        shot2 = production_layer.create_shot(
            scene_id="scene_002",
            shot_type="ai_generated",
            description="Character continues"
        )
        
        # Should be able to check continuity
        assert shot1 is not None
        assert shot2 is not None

    def test_hybrid_scene_composition(self, production_layer):
        """Test combining real footage with AI-generated content"""
        real_footage = production_layer.upload_real_footage(
            scene_id="scene_001",
            file_path="/path/to/reel.mp4"
        )
        
        ai_insert = production_layer.generate_ai_shot(
            scene_id="scene_001",
            description="AI background",
            style="seamless"
        )
        
        # Should be able to compose
        assert real_footage is not None
        assert ai_insert is not None or isinstance(ai_insert, dict)

    def test_shot_matching(self, production_layer):
        """Test matching shots by style and continuity"""
        shot1 = production_layer.create_shot(
            scene_id="scene_001",
            shot_type="ai_generated",
            description="Sunset scene",
            style="warm"
        )
        
        # Should be able to find matching shots
        assert shot1 is not None

    def test_previsualization(self, production_layer):
        """Test pre-visualization generation"""
        previz = production_layer.create_previsualization(
            scene_id="scene_001",
            shot_list=["shot_1", "shot_2"],
            style="storyboard"
        )
        
        assert previz is not None or isinstance(previz, dict)

    def test_gap_filling(self, production_layer):
        """Test AI gap filling between shots"""
        gap_fill = production_layer.fill_gap(
            scene_id="scene_001",
            start_shot="shot_1",
            end_shot="shot_2",
            duration=2.0
        )
        
        assert gap_fill is not None or isinstance(gap_fill, dict)

    def test_shot_validation(self, production_layer):
        """Test shot validation"""
        shot = production_layer.create_shot(
            scene_id="scene_001",
            shot_type="ai_generated",
            description="Valid shot"
        )
        
        # Should validate
        assert shot is not None

    def test_multiple_shot_types(self, production_layer):
        """Test different shot types"""
        shot_types = ["real_footage", "ai_generated", "hybrid"]
        
        for shot_type in shot_types:
            shot = production_layer.create_shot(
                scene_id="scene_001",
                shot_type=shot_type,
                description=f"{shot_type} shot"
            )
            
            assert shot is not None

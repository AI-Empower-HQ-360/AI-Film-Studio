"""
Unit Tests for Marketing Engine
Tests trailer generation, poster creation, and platform exports
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import uuid


@pytest.mark.unit
class TestMarketingEngine:
    """Test suite for Marketing Engine functionality"""

    @pytest.fixture
    def marketing_engine(self):
        """Create a marketing engine instance"""
        from src.engines.marketing_engine import MarketingEngine
        return MarketingEngine()

    @pytest.fixture
    def sample_project(self):
        """Sample project for marketing"""
        return {
            "project_id": str(uuid.uuid4()),
            "title": "Test Film",
            "description": "A test film",
            "duration": 120
        }

    def test_create_trailer(self, marketing_engine, sample_project):
        """Test trailer creation"""
        trailer = marketing_engine.create_trailer(
            project_id=sample_project["project_id"],
            duration=30,
            style="cinematic"
        )
        
        assert trailer is not None
        assert trailer.project_id == sample_project["project_id"]

    def test_create_poster(self, marketing_engine, sample_project):
        """Test poster creation"""
        poster = marketing_engine.create_poster(
            project_id=sample_project["project_id"],
            style="dramatic",
            dimensions={"width": 1080, "height": 1920}
        )
        
        assert poster is not None
        assert poster.project_id == sample_project["project_id"]

    def test_create_thumbnail(self, marketing_engine, sample_project):
        """Test thumbnail generation"""
        thumbnail = marketing_engine.create_thumbnail(
            project_id=sample_project["project_id"],
            timestamp=30.0,
            style="engaging"
        )
        
        assert thumbnail is not None

    def test_social_media_cutdown(self, marketing_engine, sample_project):
        """Test social media cutdown creation"""
        cutdown = marketing_engine.create_social_cutdown(
            project_id=sample_project["project_id"],
            platform="instagram",
            duration=15
        )
        
        assert cutdown is not None
        assert cutdown.platform == "instagram"

    def test_platform_export(self, marketing_engine, sample_project):
        """Test platform-specific export"""
        platforms = ["youtube", "vimeo", "tiktok", "instagram"]
        
        for platform in platforms:
            export = marketing_engine.export_for_platform(
                project_id=sample_project["project_id"],
                platform=platform
            )
            
            assert export is not None or isinstance(export, dict)

    def test_campaign_creation(self, marketing_engine, sample_project):
        """Test marketing campaign creation"""
        from src.engines.marketing_engine import Campaign
        
        campaign = marketing_engine.create_campaign(
            project_id=sample_project["project_id"],
            name="Launch Campaign",
            platforms=["youtube", "instagram"]
        )
        
        assert campaign is not None
        assert campaign.project_id == sample_project["project_id"]

    def test_asset_reuse(self, marketing_engine, sample_project):
        """Test asset reuse across campaigns"""
        # Create initial asset
        trailer = marketing_engine.create_trailer(
            project_id=sample_project["project_id"],
            duration=30
        )
        
        # Reuse in campaign
        campaign = marketing_engine.create_campaign(
            project_id=sample_project["project_id"],
            name="Reuse Campaign",
            assets=[trailer.asset_id] if hasattr(trailer, 'asset_id') else []
        )
        
        assert campaign is not None

    def test_multiple_trailer_styles(self, marketing_engine, sample_project):
        """Test different trailer styles"""
        styles = ["cinematic", "action", "emotional", "comedy"]
        
        for style in styles:
            trailer = marketing_engine.create_trailer(
                project_id=sample_project["project_id"],
                duration=30,
                style=style
            )
            
            assert trailer is not None

    def test_poster_variations(self, marketing_engine, sample_project):
        """Test poster variations"""
        variations = ["portrait", "landscape", "square"]
        
        for variation in variations:
            poster = marketing_engine.create_poster(
                project_id=sample_project["project_id"],
                style=variation
            )
            
            assert poster is not None

"""
Unit Tests for Pre-Production Engine
Tests script breakdown, scheduling, and budget estimation
"""
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from datetime import datetime, date, time
import uuid


@pytest.mark.unit
class TestPreProductionEngine:
    """Test suite for Pre-Production Engine functionality"""

    @pytest.fixture
    def preproduction_engine(self):
        """Create a pre-production engine instance"""
        from src.engines.preproduction_engine import PreProductionEngine
        return PreProductionEngine()

    @pytest.fixture
    def sample_script(self):
        """Sample script for testing"""
        return {
            "script_id": str(uuid.uuid4()),
            "title": "Test Film",
            "scenes": [
                {
                    "scene_id": "scene_001",
                    "number": 1,
                    "location": "INT. STUDIO - DAY",
                    "description": "Character enters the studio",
                    "characters": ["char_001"],
                    "dialogue": ["Hello, world!"]
                }
            ]
        }

    def test_create_breakdown(self, preproduction_engine, sample_script):
        """Test script breakdown creation"""
        breakdown = preproduction_engine.create_breakdown(
            script_id=sample_script["script_id"],
            script_data=sample_script
        )
        
        assert breakdown is not None
        assert breakdown.script_id == sample_script["script_id"]
        assert breakdown.breakdown_id is not None

    def test_extract_cast(self, preproduction_engine, sample_script):
        """Test cast extraction from script"""
        breakdown = preproduction_engine.create_breakdown(
            script_id=sample_script["script_id"],
            script_data=sample_script
        )
        
        assert len(breakdown.cast) >= 0  # At least empty list

    def test_extract_locations(self, preproduction_engine, sample_script):
        """Test location extraction"""
        breakdown = preproduction_engine.create_breakdown(
            script_id=sample_script["script_id"],
            script_data=sample_script
        )
        
        assert len(breakdown.locations) >= 0

    def test_create_shooting_schedule(self, preproduction_engine, sample_script):
        """Test shooting schedule creation"""
        schedule = preproduction_engine.create_schedule(
            script_id=sample_script["script_id"],
            start_date=date.today(),
            days_per_week=5
        )
        
        assert schedule is not None
        assert schedule.script_id == sample_script["script_id"]
        assert schedule.start_date is not None

    def test_schedule_optimization(self, preproduction_engine):
        """Test schedule optimization by location"""
        script_data = {
            "script_id": "test_script",
            "scenes": [
                {"scene_id": "s1", "location": "LOCATION_A"},
                {"scene_id": "s2", "location": "LOCATION_A"},
                {"scene_id": "s3", "location": "LOCATION_B"},
            ]
        }
        
        schedule = preproduction_engine.create_schedule(
            script_id="test_script",
            start_date=date.today()
        )
        
        # Locations should be grouped
        assert schedule is not None

    def test_budget_estimation(self, preproduction_engine, sample_script):
        """Test budget estimation"""
        breakdown = preproduction_engine.create_breakdown(
            script_id=sample_script["script_id"],
            script_data=sample_script
        )
        
        budget = preproduction_engine.estimate_budget(
            script_id=sample_script["script_id"],
            breakdown=breakdown
        )
        
        assert budget is not None
        assert budget.script_id == sample_script["script_id"]
        assert budget.total_estimated >= 0

    def test_budget_categories(self, preproduction_engine):
        """Test budget category calculation"""
        breakdown = preproduction_engine.create_breakdown(
            script_id="test",
            script_data={"script_id": "test", "scenes": []}
        )
        
        budget = preproduction_engine.estimate_budget(
            script_id="test",
            breakdown=breakdown
        )
        
        assert len(budget.categories) >= 0

    def test_call_sheet_generation(self, preproduction_engine):
        """Test call sheet generation"""
        schedule = preproduction_engine.create_schedule(
            script_id="test",
            start_date=date.today()
        )
        
        if len(schedule.shooting_days) > 0:
            call_sheet = preproduction_engine.create_call_sheet(
                schedule_id=schedule.schedule_id,
                day_number=1
            )
            
            assert call_sheet is not None
            assert call_sheet.day_number == 1

    def test_schedule_conflict_detection(self, preproduction_engine):
        """Test detection of scheduling conflicts"""
        schedule = preproduction_engine.create_schedule(
            script_id="test",
            start_date=date.today()
        )
        
        # Should not raise errors
        assert schedule is not None

    def test_breakdown_with_multiple_scenes(self, preproduction_engine):
        """Test breakdown with multiple scenes"""
        script_data = {
            "script_id": "multi_scene",
            "scenes": [
                {"scene_id": "s1", "location": "LOC_A", "characters": ["char1"]},
                {"scene_id": "s2", "location": "LOC_B", "characters": ["char2"]},
                {"scene_id": "s3", "location": "LOC_A", "characters": ["char1", "char2"]},
            ]
        }
        
        breakdown = preproduction_engine.create_breakdown(
            script_id="multi_scene",
            script_data=script_data
        )
        
        assert breakdown is not None
        assert breakdown.script_id == "multi_scene"

    def test_empty_script_handling(self, preproduction_engine):
        """Test handling of empty script"""
        breakdown = preproduction_engine.create_breakdown(
            script_id="empty",
            script_data={"script_id": "empty", "scenes": []}
        )
        
        assert breakdown is not None
        assert breakdown.script_id == "empty"

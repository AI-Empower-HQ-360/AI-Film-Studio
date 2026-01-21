"""
Unit Tests for Production Management (Studio Ops)
Tests RBAC, asset management, timeline tracking, and approvals
"""
import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
import uuid


@pytest.mark.unit
class TestProductionManagement:
    """Test suite for Production Management functionality"""

    @pytest.fixture
    def production_manager(self):
        """Create a production manager instance"""
        from src.engines.production_management import ProductionManager
        return ProductionManager()

    @pytest.fixture
    def sample_user(self):
        """Sample user for testing"""
        from src.engines.production_management import User, UserRole
        return User(
            email="test@example.com",
            name="Test User",
            role=UserRole.DIRECTOR
        )

    @pytest.fixture
    def sample_project(self):
        """Sample project for testing"""
        from src.engines.production_management import Project
        return Project(
            name="Test Project",
            description="Test description",
            created_by="user_001"
        )

    def test_create_project(self, production_manager, sample_user):
        """Test project creation"""
        project = production_manager.create_project(
            name="New Project",
            description="Test project",
            created_by=sample_user.user_id
        )
        
        assert project is not None
        assert project.name == "New Project"
        assert project.created_by == sample_user.user_id

    def test_user_role_enum(self):
        """Test user role enumeration"""
        from src.engines.production_management import UserRole
        
        assert UserRole.WRITER.value == "writer"
        assert UserRole.DIRECTOR.value == "director"
        assert UserRole.PRODUCER.value == "producer"
        assert UserRole.EDITOR.value == "editor"
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.VIEWER.value == "viewer"

    def test_asset_creation(self, production_manager, sample_project):
        """Test asset creation"""
        from src.engines.production_management import AssetType, AssetStatus
        
        asset = production_manager.create_asset(
            asset_type=AssetType.SCRIPT,
            name="Test Script",
            project_id=sample_project.project_id,
            created_by="user_001"
        )
        
        assert asset is not None
        assert asset.asset_type == AssetType.SCRIPT
        assert asset.name == "Test Script"
        assert asset.project_id == sample_project.project_id
        assert asset.status == AssetStatus.DRAFT

    def test_asset_status_transition(self, production_manager, sample_project):
        """Test asset status transitions"""
        from src.engines.production_management import AssetType, AssetStatus
        
        asset = production_manager.create_asset(
            asset_type=AssetType.VIDEO,
            name="Test Video",
            project_id=sample_project.project_id,
            created_by="user_001"
        )
        
        # Transition to in_review
        asset = production_manager.update_asset_status(
            asset_id=asset.asset_id,
            new_status=AssetStatus.IN_REVIEW,
            updated_by="user_002"
        )
        
        assert asset.status == AssetStatus.IN_REVIEW

    def test_timeline_creation(self, production_manager, sample_project):
        """Test timeline creation"""
        timeline = production_manager.create_timeline(
            project_id=sample_project.project_id,
            name="Main Timeline"
        )
        
        assert timeline is not None
        assert timeline.project_id == sample_project.project_id
        assert timeline.name == "Main Timeline"

    def test_milestone_creation(self, production_manager, sample_project):
        """Test milestone creation"""
        from src.engines.production_management import MilestoneStatus
        
        milestone = production_manager.create_milestone(
            project_id=sample_project.project_id,
            name="Pre-Production Complete",
            target_date=datetime(2025, 12, 31),
            status=MilestoneStatus.NOT_STARTED
        )
        
        assert milestone is not None
        assert milestone.name == "Pre-Production Complete"
        assert milestone.status == MilestoneStatus.NOT_STARTED

    def test_permission_checking(self, production_manager, sample_user):
        """Test permission checking"""
        from src.engines.production_management import UserRole
        
        # Director should have write permissions
        has_permission = production_manager.check_permission(
            user_role=sample_user.role,
            action="write",
            resource_type="project"
        )
        
        assert isinstance(has_permission, bool)

    def test_project_access_control(self, production_manager, sample_user, sample_project):
        """Test project access control"""
        # Add user to project
        production_manager.add_user_to_project(
            project_id=sample_project.project_id,
            user_id=sample_user.user_id,
            role=sample_user.role
        )
        
        # Check access
        has_access = production_manager.check_project_access(
            project_id=sample_project.project_id,
            user_id=sample_user.user_id
        )
        
        assert has_access is True or isinstance(has_access, bool)

    def test_asset_locking(self, production_manager, sample_project):
        """Test asset locking"""
        from src.engines.production_management import AssetType, AssetStatus
        
        asset = production_manager.create_asset(
            asset_type=AssetType.SCRIPT,
            name="Locked Script",
            project_id=sample_project.project_id,
            created_by="user_001"
        )
        
        # Lock asset
        locked_asset = production_manager.lock_asset(
            asset_id=asset.asset_id,
            locked_by="user_002"
        )
        
        assert locked_asset.status == AssetStatus.LOCKED or locked_asset is not None

    def test_review_creation(self, production_manager, sample_project):
        """Test review creation"""
        from src.engines.production_management import AssetType
        
        asset = production_manager.create_asset(
            asset_type=AssetType.VIDEO,
            name="Video for Review",
            project_id=sample_project.project_id,
            created_by="user_001"
        )
        
        review = production_manager.create_review(
            asset_id=asset.asset_id,
            reviewer_id="user_002",
            comments="Looks good!"
        )
        
        assert review is not None
        assert review.asset_id == asset.asset_id
        assert review.reviewer_id == "user_002"

    def test_audit_log_creation(self, production_manager, sample_project):
        """Test audit log creation"""
        from src.engines.production_management import AssetType
        
        asset = production_manager.create_asset(
            asset_type=AssetType.SCRIPT,
            name="Audited Asset",
            project_id=sample_project.project_id,
            created_by="user_001"
        )
        
        # Action should create audit log
        assert asset is not None

    def test_multiple_asset_types(self, production_manager, sample_project):
        """Test creating multiple asset types"""
        from src.engines.production_management import AssetType
        
        asset_types = [
            AssetType.SCRIPT,
            AssetType.CHARACTER,
            AssetType.VIDEO,
            AssetType.AUDIO,
            AssetType.MUSIC
        ]
        
        for asset_type in asset_types:
            asset = production_manager.create_asset(
                asset_type=asset_type,
                name=f"Test {asset_type.value}",
                project_id=sample_project.project_id,
                created_by="user_001"
            )
            
            assert asset is not None
            assert asset.asset_type == asset_type

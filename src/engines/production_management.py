"""
Production Management - Studio Operations
Enterprise studio control layer with RBAC, asset management, and workflows
"""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class UserRole(str, Enum):
    """User roles in studio"""
    WRITER = "writer"
    DIRECTOR = "director"
    PRODUCER = "producer"
    EDITOR = "editor"
    ADMIN = "admin"
    VIEWER = "viewer"


class AssetType(str, Enum):
    """Asset types"""
    SCRIPT = "script"
    CHARACTER = "character"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    MUSIC = "music"
    SUBTITLE = "subtitle"
    DOCUMENT = "document"


class AssetStatus(str, Enum):
    """Asset status"""
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    LOCKED = "locked"
    ARCHIVED = "archived"


class MilestoneStatus(str, Enum):
    """Milestone status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class User(BaseModel):
    """User with role-based access"""
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    name: str
    role: UserRole
    organization_id: Optional[str] = None
    permissions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Asset(BaseModel):
    """Production asset"""
    asset_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_type: AssetType
    name: str
    s3_key: Optional[str] = None
    url: Optional[str] = None
    project_id: str
    status: AssetStatus = AssetStatus.DRAFT
    version: str = "1.0"
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class Milestone(BaseModel):
    """Project milestone"""
    milestone_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    name: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: MilestoneStatus = MilestoneStatus.NOT_STARTED
    assigned_to: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)  # Other milestone IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Approval(BaseModel):
    """Approval record"""
    approval_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    asset_id: str
    approver_id: str
    status: str  # approved, rejected, pending
    comments: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Timeline(BaseModel):
    """Project timeline with milestones"""
    timeline_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    milestones: List[Milestone] = Field(default_factory=list)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Project(BaseModel):
    """Production project"""
    project_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    organization_id: Optional[str] = None
    script_id: Optional[str] = None
    production_plan_id: Optional[str] = None
    status: str = "draft"  # draft, pre-production, production, post-production, completed
    created_by: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AuditLog(BaseModel):
    """Audit log entry"""
    log_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    user_id: str
    action: str
    resource_type: str
    resource_id: str
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ProductionManager:
    """
    Production Management - Studio Operations
    
    Enterprise studio control layer:
    - Role-based access control (writer, director, producer, editor)
    - Asset management (scripts, footage, audio, images)
    - Timeline & milestone tracking
    - Review, approval, and locking
    - Audit logs and compliance
    """
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.assets: Dict[str, Asset] = {}
        self.users: Dict[str, User] = {}
        self.timelines: Dict[str, Timeline] = {}
        self.approvals: Dict[str, Approval] = {}
        self.audit_logs: List[AuditLog] = []
    
    async def create_project(
        self,
        name: str,
        created_by: str,
        description: Optional[str] = None,
        organization_id: Optional[str] = None
    ) -> Project:
        """Create a new production project"""
        project = Project(
            name=name,
            description=description,
            created_by=created_by,
            organization_id=organization_id
        )
        
        self.projects[project.project_id] = project
        
        # Create timeline
        timeline = Timeline(project_id=project.project_id)
        self.timelines[project.project_id] = timeline
        
        self._log_audit(
            project.project_id,
            created_by,
            "create_project",
            "project",
            project.project_id
        )
        
        logger.info(f"Created project {project.project_id}: {name}")
        
        return project
    
    async def add_asset(
        self,
        project_id: str,
        asset_type: AssetType,
        name: str,
        created_by: str,
        s3_key: Optional[str] = None,
        url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Asset:
        """Add asset to project"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        asset = Asset(
            asset_type=asset_type,
            name=name,
            project_id=project_id,
            created_by=created_by,
            s3_key=s3_key,
            url=url,
            metadata=metadata or {}
        )
        
        self.assets[asset.asset_id] = asset
        
        self._log_audit(
            project_id,
            created_by,
            "add_asset",
            "asset",
            asset.asset_id,
            {"asset_type": asset_type.value, "name": name}
        )
        
        logger.info(f"Added asset {asset.asset_id} to project {project_id}")
        
        return asset
    
    async def create_milestone(
        self,
        project_id: str,
        name: str,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        assigned_to: Optional[str] = None
    ) -> Milestone:
        """Create milestone in project timeline"""
        if project_id not in self.timelines:
            raise ValueError(f"Timeline for project {project_id} not found")
        
        timeline = self.timelines[project_id]
        
        milestone = Milestone(
            project_id=project_id,
            name=name,
            description=description,
            due_date=due_date,
            assigned_to=assigned_to
        )
        
        timeline.milestones.append(milestone)
        
        logger.info(f"Created milestone {milestone.milestone_id} for project {project_id}")
        
        return milestone
    
    async def request_approval(
        self,
        asset_id: str,
        approver_id: str,
        comments: Optional[str] = None
    ) -> Approval:
        """Request approval for an asset"""
        if asset_id not in self.assets:
            raise ValueError(f"Asset {asset_id} not found")
        
        asset = self.assets[asset_id]
        asset.status = AssetStatus.IN_REVIEW
        
        approval = Approval(
            asset_id=asset_id,
            approver_id=approver_id,
            status="pending",
            comments=comments
        )
        
        self.approvals[approval.approval_id] = approval
        
        logger.info(f"Requested approval for asset {asset_id}")
        
        return approval
    
    async def approve_asset(
        self,
        approval_id: str,
        approver_id: str,
        approved: bool,
        comments: Optional[str] = None
    ) -> Approval:
        """Approve or reject an asset"""
        if approval_id not in self.approvals:
            raise ValueError(f"Approval {approval_id} not found")
        
        approval = self.approvals[approval_id]
        
        if approval.approver_id != approver_id:
            raise ValueError("Approver ID mismatch")
        
        approval.status = "approved" if approved else "rejected"
        approval.comments = comments
        
        asset = self.assets[approval.asset_id]
        if approved:
            asset.status = AssetStatus.APPROVED
        else:
            asset.status = AssetStatus.DRAFT
        
        self._log_audit(
            asset.project_id,
            approver_id,
            "approve_asset" if approved else "reject_asset",
            "asset",
            asset.asset_id
        )
        
        logger.info(f"Asset {asset.asset_id} {'approved' if approved else 'rejected'}")
        
        return approval
    
    async def lock_asset(
        self,
        asset_id: str,
        user_id: str
    ) -> Asset:
        """Lock an asset (prevent further edits)"""
        if asset_id not in self.assets:
            raise ValueError(f"Asset {asset_id} not found")
        
        asset = self.assets[asset_id]
        asset.status = AssetStatus.LOCKED
        
        self._log_audit(
            asset.project_id,
            user_id,
            "lock_asset",
            "asset",
            asset_id
        )
        
        logger.info(f"Locked asset {asset_id}")
        
        return asset
    
    def _log_audit(
        self,
        project_id: str,
        user_id: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Log audit event"""
        log = AuditLog(
            project_id=project_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {}
        )
        
        self.audit_logs.append(log)
    
    async def get_project_assets(
        self,
        project_id: str,
        asset_type: Optional[AssetType] = None,
        status: Optional[AssetStatus] = None
    ) -> List[Asset]:
        """Get all assets for a project with optional filters"""
        assets = [a for a in self.assets.values() if a.project_id == project_id]
        
        if asset_type:
            assets = [a for a in assets if a.asset_type == asset_type]
        
        if status:
            assets = [a for a in assets if a.status == status]
        
        return assets
    
    async def get_project(self, project_id: str) -> Project:
        """Get project by ID"""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        return self.projects[project_id]
    
    async def get_timeline(self, project_id: str) -> Timeline:
        """Get project timeline"""
        if project_id not in self.timelines:
            raise ValueError(f"Timeline for project {project_id} not found")
        return self.timelines[project_id]
    
    async def check_permission(
        self,
        user_id: str,
        project_id: str,
        action: str
    ) -> bool:
        """Check if user has permission for action"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        project = self.projects.get(project_id)
        
        if not project:
            return False
        
        # Role-based permissions
        role_permissions = {
            UserRole.ADMIN: ["all"],
            UserRole.PRODUCER: ["approve", "lock", "view", "edit"],
            UserRole.DIRECTOR: ["approve", "view", "edit"],
            UserRole.EDITOR: ["view", "edit"],
            UserRole.WRITER: ["view", "edit"],
            UserRole.VIEWER: ["view"]
        }
        
        perms = role_permissions.get(user.role, [])
        
        if "all" in perms:
            return True
        
        return action in perms

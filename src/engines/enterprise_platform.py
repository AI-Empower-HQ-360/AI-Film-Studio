"""
Enterprise Platform Layer
SaaS governance, multi-tenancy, billing, API access, security
"""
from typing import Optional, Dict, List, Any
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class SubscriptionTier(str, Enum):
    """Subscription tiers"""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class UsageMetric(str, Enum):
    """Usage metrics"""
    VIDEO_MINUTES = "video_minutes"
    CHARACTER_GENERATIONS = "character_generations"
    VOICE_MINUTES = "voice_minutes"
    MUSIC_MINUTES = "music_minutes"
    API_CALLS = "api_calls"
    STORAGE_GB = "storage_gb"


class Organization(BaseModel):
    """Organization/tenant"""
    organization_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class UsageRecord(BaseModel):
    """Usage record for billing"""
    record_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    metric: UsageMetric
    quantity: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    project_id: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class BillingPeriod(BaseModel):
    """Billing period"""
    period_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    start_date: datetime
    end_date: datetime
    usage: Dict[str, float] = Field(default_factory=dict)  # metric -> quantity
    cost: float = 0.0
    currency: str = "USD"
    status: str = "pending"  # pending, paid, overdue


class APIKey(BaseModel):
    """API key for programmatic access"""
    key_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    key_hash: str  # Hashed API key
    name: str
    permissions: List[str] = Field(default_factory=list)
    rate_limit: int = 1000  # Requests per hour
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = True


class SLA(BaseModel):
    """Service Level Agreement"""
    sla_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str
    uptime_target: float = 99.9  # Percentage
    response_time_ms: int = 500
    support_level: str = "standard"  # standard, priority, dedicated
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EnterprisePlatform:
    """
    Enterprise Platform Layer
    
    SaaS governance and scalability:
    - Multi-tenant organizations
    - Usage metering and billing
    - API access
    - Data isolation
    - Security, compliance, SLAs
    """
    
    def __init__(self):
        self.organizations: Dict[str, Organization] = {}
        self.usage_records: List[UsageRecord] = []
        self.billing_periods: Dict[str, BillingPeriod] = {}
        self.api_keys: Dict[str, APIKey] = {}
        self.slas: Dict[str, SLA] = {}
    
    async def create_organization(
        self,
        name: str,
        subscription_tier: SubscriptionTier = SubscriptionTier.FREE
    ) -> Organization:
        """Create new organization/tenant"""
        org = Organization(
            name=name,
            subscription_tier=subscription_tier
        )
        
        self.organizations[org.organization_id] = org
        
        # Create SLA
        sla = SLA(organization_id=org.organization_id)
        self.slas[org.organization_id] = sla
        
        logger.info(f"Created organization {org.organization_id}: {name}")
        
        return org
    
    async def record_usage(
        self,
        organization_id: str,
        metric: UsageMetric,
        quantity: float,
        project_id: Optional[str] = None
    ) -> UsageRecord:
        """Record usage for billing"""
        if organization_id not in self.organizations:
            raise ValueError(f"Organization {organization_id} not found")
        
        record = UsageRecord(
            organization_id=organization_id,
            metric=metric,
            quantity=quantity,
            project_id=project_id
        )
        
        self.usage_records.append(record)
        
        logger.info(f"Recorded {quantity} {metric.value} for organization {organization_id}")
        
        return record
    
    async def get_usage_summary(
        self,
        organization_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, float]:
        """Get usage summary for organization"""
        records = [
            r for r in self.usage_records
            if r.organization_id == organization_id
        ]
        
        if start_date:
            records = [r for r in records if r.timestamp >= start_date]
        
        if end_date:
            records = [r for r in records if r.timestamp <= end_date]
        
        summary = {}
        for record in records:
            metric = record.metric.value
            summary[metric] = summary.get(metric, 0.0) + record.quantity
        
        return summary
    
    async def calculate_billing(
        self,
        organization_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> BillingPeriod:
        """Calculate billing for period"""
        if organization_id not in self.organizations:
            raise ValueError(f"Organization {organization_id} not found")
        
        org = self.organizations[organization_id]
        
        # Get usage for period
        usage_summary = await self.get_usage_summary(organization_id, start_date, end_date)
        
        # Calculate cost based on tier and usage
        cost = self._calculate_cost(org.subscription_tier, usage_summary)
        
        period = BillingPeriod(
            organization_id=organization_id,
            start_date=start_date,
            end_date=end_date,
            usage=usage_summary,
            cost=cost
        )
        
        self.billing_periods[period.period_id] = period
        
        logger.info(f"Calculated billing ${cost:.2f} for organization {organization_id}")
        
        return period
    
    def _calculate_cost(
        self,
        tier: SubscriptionTier,
        usage: Dict[str, float]
    ) -> float:
        """Calculate cost based on tier and usage"""
        # Pricing model:
        # Free: Limited usage, pay-as-you-go after limits
        # Pro: Monthly fee + usage credits
        # Enterprise: Custom pricing
        
        base_cost = {
            SubscriptionTier.FREE: 0.0,
            SubscriptionTier.PRO: 99.0,
            SubscriptionTier.ENTERPRISE: 0.0  # Custom
        }
        
        cost = base_cost.get(tier, 0.0)
        
        # Usage-based pricing
        usage_rates = {
            UsageMetric.VIDEO_MINUTES.value: 0.10,  # $0.10 per minute
            UsageMetric.VOICE_MINUTES.value: 0.05,
            UsageMetric.MUSIC_MINUTES.value: 0.03,
            UsageMetric.CHARACTER_GENERATIONS.value: 0.50,
            UsageMetric.API_CALLS.value: 0.001,
            UsageMetric.STORAGE_GB.value: 0.10
        }
        
        for metric, quantity in usage.items():
            rate = usage_rates.get(metric, 0.0)
            cost += quantity * rate
        
        return cost
    
    async def create_api_key(
        self,
        organization_id: str,
        name: str,
        permissions: Optional[List[str]] = None,
        rate_limit: int = 1000
    ) -> APIKey:
        """Create API key for programmatic access"""
        if organization_id not in self.organizations:
            raise ValueError(f"Organization {organization_id} not found")
        
        key_id = str(uuid.uuid4())
        # In production, would hash the actual key
        key_hash = f"hash_{key_id}"
        
        api_key = APIKey(
            organization_id=organization_id,
            key_hash=key_hash,
            name=name,
            permissions=permissions or ["read", "write"],
            rate_limit=rate_limit
        )
        
        self.api_keys[api_key.key_id] = api_key
        
        logger.info(f"Created API key {api_key.key_id} for organization {organization_id}")
        
        return api_key
    
    async def validate_api_key(self, key_hash: str) -> Optional[APIKey]:
        """Validate API key"""
        for key in self.api_keys.values():
            if key.key_hash == key_hash and key.is_active:
                if key.expires_at and key.expires_at < datetime.utcnow():
                    return None
                return key
        return None
    
    async def get_organization(self, organization_id: str) -> Organization:
        """Get organization by ID"""
        if organization_id not in self.organizations:
            raise ValueError(f"Organization {organization_id} not found")
        return self.organizations[organization_id]
    
    async def ensure_data_isolation(
        self,
        organization_id: str,
        resource_id: str
    ) -> bool:
        """Ensure resource belongs to organization (data isolation)"""
        # In production, would check database/access control
        # For now, return True
        return True

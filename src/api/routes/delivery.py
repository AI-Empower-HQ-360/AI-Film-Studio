"""
Delivery Routes - API endpoints for multi-platform delivery
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/delivery", tags=["delivery"])


class DeliveryRequest(BaseModel):
    """Request model for delivery"""
    export_id: str = Field(...)
    platforms: List[str] = Field(default=["youtube"])
    schedule_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None


class DeliveryResponse(BaseModel):
    """Response model for delivery"""
    delivery_id: str
    export_id: str
    platforms: List[str]
    status: str
    results: Optional[Dict[str, Any]] = None
    created_at: datetime


class DeliveryService:
    """Service class for delivery operations"""
    
    SUPPORTED_PLATFORMS = ["youtube", "tiktok", "instagram", "twitter", "vimeo"]
    
    def __init__(self):
        self.deliveries: Dict[str, Dict[str, Any]] = {}
    
    async def create_delivery(
        self,
        export_id: str,
        platforms: List[str],
        schedule_at: Optional[datetime] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Create a delivery job"""
        delivery_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        # Validate platforms
        for platform in platforms:
            if platform not in self.SUPPORTED_PLATFORMS:
                raise ValueError(f"Unsupported platform: {platform}")
        
        delivery = {
            "delivery_id": delivery_id,
            "export_id": export_id,
            "platforms": platforms,
            "schedule_at": schedule_at,
            "metadata": metadata or {},
            "status": "pending" if schedule_at else "processing",
            "results": {},
            "created_at": now,
        }
        
        self.deliveries[delivery_id] = delivery
        return delivery
    
    async def get_delivery(self, delivery_id: str) -> Optional[Dict[str, Any]]:
        """Get delivery by ID"""
        return self.deliveries.get(delivery_id)
    
    async def list_deliveries(
        self,
        export_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List deliveries, optionally filtered by export"""
        all_deliveries = list(self.deliveries.values())
        if export_id:
            all_deliveries = [d for d in all_deliveries if d["export_id"] == export_id]
        return all_deliveries
    
    async def cancel_delivery(self, delivery_id: str) -> bool:
        """Cancel a scheduled delivery"""
        if delivery_id in self.deliveries:
            self.deliveries[delivery_id]["status"] = "cancelled"
            return True
        return False


# Global service instance
_delivery_service = DeliveryService()


def get_delivery_service() -> DeliveryService:
    """Dependency injection for delivery service"""
    return _delivery_service


@router.post("/", response_model=DeliveryResponse)
async def create_delivery(
    request: DeliveryRequest,
    service: DeliveryService = Depends(get_delivery_service)
):
    """Create a delivery job"""
    try:
        result = await service.create_delivery(
            export_id=request.export_id,
            platforms=request.platforms,
            schedule_at=request.schedule_at,
            metadata=request.metadata
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{delivery_id}", response_model=DeliveryResponse)
async def get_delivery(
    delivery_id: str,
    service: DeliveryService = Depends(get_delivery_service)
):
    """Get delivery by ID"""
    delivery = await service.get_delivery(delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery


@router.get("/", response_model=List[DeliveryResponse])
async def list_deliveries(
    export_id: Optional[str] = None,
    service: DeliveryService = Depends(get_delivery_service)
):
    """List all deliveries"""
    return await service.list_deliveries(export_id=export_id)


@router.post("/{delivery_id}/cancel")
async def cancel_delivery(
    delivery_id: str,
    service: DeliveryService = Depends(get_delivery_service)
):
    """Cancel a scheduled delivery"""
    success = await service.cancel_delivery(delivery_id)
    if not success:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return {"status": "cancelled"}

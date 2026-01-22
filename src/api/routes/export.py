"""
Export Routes - API endpoints for exporting videos/projects
"""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/export", tags=["export"])


class ExportRequest(BaseModel):
    """Request model for export"""
    project_id: str = Field(...)
    format: str = Field(default="mp4")
    resolution: str = Field(default="1080p")
    include_subtitles: bool = Field(default=False)


class ExportResponse(BaseModel):
    """Response model for export"""
    export_id: str
    project_id: str
    status: str
    format: str
    resolution: str
    url: Optional[str] = None
    created_at: datetime


class ExportService:
    """Service class for export operations"""
    
    def __init__(self):
        self.exports: Dict[str, Dict[str, Any]] = {}
    
    async def create_export(
        self,
        project_id: str,
        format: str = "mp4",
        resolution: str = "1080p",
        include_subtitles: bool = False
    ) -> Dict[str, Any]:
        """Create an export job"""
        export_id = str(uuid.uuid4())
        now = datetime.utcnow()
        
        export = {
            "export_id": export_id,
            "project_id": project_id,
            "format": format,
            "resolution": resolution,
            "include_subtitles": include_subtitles,
            "status": "processing",
            "url": None,
            "created_at": now,
        }
        
        self.exports[export_id] = export
        return export
    
    async def get_export(self, export_id: str) -> Optional[Dict[str, Any]]:
        """Get export by ID"""
        return self.exports.get(export_id)
    
    async def list_exports(
        self,
        project_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List exports, optionally filtered by project"""
        all_exports = list(self.exports.values())
        if project_id:
            all_exports = [e for e in all_exports if e["project_id"] == project_id]
        return all_exports


# Global service instance
_export_service = ExportService()


def get_export_service() -> ExportService:
    """Dependency injection for export service"""
    return _export_service


@router.post("/", response_model=ExportResponse)
async def create_export(
    request: ExportRequest,
    service: ExportService = Depends(get_export_service)
):
    """Create an export job"""
    result = await service.create_export(
        project_id=request.project_id,
        format=request.format,
        resolution=request.resolution,
        include_subtitles=request.include_subtitles
    )
    return result


@router.get("/{export_id}", response_model=ExportResponse)
async def get_export(
    export_id: str,
    service: ExportService = Depends(get_export_service)
):
    """Get export by ID"""
    export = await service.get_export(export_id)
    if not export:
        raise HTTPException(status_code=404, detail="Export not found")
    return export


@router.get("/", response_model=List[ExportResponse])
async def list_exports(
    project_id: Optional[str] = None,
    service: ExportService = Depends(get_export_service)
):
    """List all exports"""
    return await service.list_exports(project_id=project_id)

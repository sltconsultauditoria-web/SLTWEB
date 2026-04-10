"""
Endpoints de Health Check
"""
from fastapi import APIRouter
from datetime import datetime
import os

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/")
async def health_check():
    """Health check básico"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "sltdctfweb-api",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health():
    """Health check detalhado"""
    from motor.motor_asyncio import AsyncIOMotorClient
    from clients.sharepoint_client import SharePointClient
    
    result = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }
    
    # Verificar MongoDB
    try:
        mongo_url = os.environ.get("MONGO_URL")
        if not mongo_url:
            raise ValueError("MONGO_URL não configurada no ambiente")
            
        client = AsyncIOMotorClient(mongo_url)
        # Timeout curto para o health check não travar a API
        await client.admin.command('ping')
        result["checks"]["mongodb"] = {"status": "ok"}
        client.close()
    except Exception as e:
        result["checks"]["mongodb"] = {"status": "error", "error": str(e)}
        result["status"] = "degraded"
    
    # Verificar SharePoint
    sp_client = SharePointClient()
    result["checks"]["sharepoint"] = {
        "configured": sp_client.is_configured,
        "status": "ok" if sp_client.is_configured else "not_configured"
    }
    
    return result
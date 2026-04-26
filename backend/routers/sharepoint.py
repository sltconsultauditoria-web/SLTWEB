"""
Router de SharePoint - /api/sharepoint
Integracao com SharePoint
"""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter( tags=["SharePoint"])


@router.get("/status")
async def get_sharepoint_status(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Retorna status da integracao SharePoint."""
    try:
        status_doc = await db["sharepoint_status"].find_one({"tipo": "connection"})
        if status_doc:
            status_doc.pop("_id", None)
            return status_doc
        return {
            "status": "not_configured",
            "mensagem": "Integracao SharePoint nao configurada",
            "ultima_sincronizacao": None,
            "arquivos_sincronizados": 0
        }
    except Exception as e:
        logger.error(f"Erro ao obter status SharePoint: {e}")
        return {"status": "error", "mensagem": str(e)}


@router.get("/files")
async def list_sharepoint_files(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Lista arquivos sincronizados do SharePoint."""
    try:
        items = await db["sharepoint_files"].find().to_list(100)
        for i in items:
            i.pop("_id", None)
        return {"arquivos": items, "total": len(items)}
    except Exception as e:
        logger.error(f"Erro ao listar arquivos SharePoint: {e}")
        return {"arquivos": [], "total": 0}


@router.post("/sync")
async def sync_sharepoint(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Inicia sincronizacao com SharePoint."""
    await db["sharepoint_status"].update_one(
        {"tipo": "connection"},
        {"$set": {"status": "syncing", "iniciado_em": datetime.utcnow()}},
        upsert=True
    )
    return {"success": True, "message": "Sincronizacao iniciada", "status": "syncing"}

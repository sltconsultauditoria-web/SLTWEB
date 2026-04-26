"""
Router de Robots - /api/robots
Controle e monitoramento dos robos de automacao
"""
import logging
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Robots"])


class RoboStatusResponse(BaseModel):
    status: str
    ultimo_run: Optional[datetime] = None
    proximo_run: Optional[datetime] = None
    arquivos_processados: int = 0
    erros: int = 0
    mensagem: Optional[str] = None


@router.get("/ingestion/status")
async def get_ingestion_status(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Retorna status do robo de ingestao."""
    try:
        status_doc = await db["robots_status"].find_one({"tipo": "ingestion"})
        if status_doc:
            status_doc.pop("_id", None)
            return status_doc
        return {
            "status": "idle",
            "tipo": "ingestion",
            "ultimo_run": None,
            "proximo_run": None,
            "arquivos_processados": 0,
            "erros": 0,
            "mensagem": "Robo de ingestao nao executado ainda"
        }
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return {"status": "error", "mensagem": str(e)}


@router.get("/ingestion/history")
async def get_ingestion_history(
    limit: int = 10,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Retorna historico de execucoes do robo."""
    try:
        items = await db["robots_history"].find(
            {"tipo": "ingestion"}
        ).sort("created_at", -1).limit(limit).to_list(limit)
        for i in items:
            i.pop("_id", None)
        return {"historico": items, "total": len(items)}
    except Exception as e:
        logger.error(f"Erro ao obter historico: {e}")
        return {"historico": [], "total": 0}


@router.get("/ingestion/files")
async def get_ingestion_files(
    limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Lista arquivos processados pelo robo."""
    try:
        items = await db["documentos"].find(
            {"origem": "ingestion"}
        ).sort("created_at", -1).limit(limit).to_list(limit)
        for i in items:
            i["id"] = str(i.get("_id", i.get("id", "")))
            i.pop("_id", None)
        return {"arquivos": items, "total": len(items)}
    except Exception as e:
        logger.error(f"Erro ao listar arquivos: {e}")
        return {"arquivos": [], "total": 0}


@router.post("/ingestion/start")
async def start_ingestion(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Inicia o robo de ingestao."""
    await db["robots_status"].update_one(
        {"tipo": "ingestion"},
        {"$set": {"status": "running", "iniciado_em": datetime.utcnow()}},
        upsert=True
    )
    return {"success": True, "message": "Robo de ingestao iniciado", "status": "running"}


@router.post("/ingestion/stop")
async def stop_ingestion(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Para o robo de ingestao."""
    await db["robots_status"].update_one(
        {"tipo": "ingestion"},
        {"$set": {"status": "stopped", "parado_em": datetime.utcnow()}},
        upsert=True
    )
    return {"success": True, "message": "Robo de ingestao parado", "status": "stopped"}


@router.post("/ingestion/run-now")
async def run_ingestion_now(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Executa o robo de ingestao imediatamente."""
    await db["robots_status"].update_one(
        {"tipo": "ingestion"},
        {"$set": {"status": "running", "iniciado_em": datetime.utcnow(), "ultimo_run": datetime.utcnow()}},
        upsert=True
    )
    return {"success": True, "message": "Execucao manual iniciada", "status": "running"}

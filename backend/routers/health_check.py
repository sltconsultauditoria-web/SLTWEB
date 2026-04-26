"""
Router de Health Check - /api/health
Verifica o status da API e da conexão com o MongoDB
"""
import logging
from datetime import datetime
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db
import time

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Health"])


@router.get("/")
async def health_check(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Verifica o status da API e do banco de dados."""
    try:
        await db.command("ping")
        db_status = "connected"
    except Exception as e:
        logger.error(f"DB health check failed: {e}")
        db_status = "disconnected"

    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "version": "1.0.0",
        "service": "ConsultSLT API"
    }

@router.get("/api/system/health")
async def health_check(db: AsyncIOMotorDatabase = Depends(get_db)):
    start_time = time.time()

    # Verificar conexão com o MongoDB
    try:
        await db.command("ping")
        mongo_status = "ok"
    except Exception as e:
        mongo_status = f"erro: {str(e)}"

    # Verificar routers ativos
    active_routers = [route.path for route in router.routes]

    # Calcular tempo de resposta
    response_time = time.time() - start_time

    return {
        "mongo_status": mongo_status,
        "active_routers": active_routers,
        "response_time": response_time
    }

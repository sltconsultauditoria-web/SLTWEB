from fastapi import APIRouter
from backend.core.database import get_db
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/")
async def dashboard(db: AsyncIOMotorDatabase = Depends(get_db)):

    empresas = await db.empresas.count_documents({})
    alertas = await db.alertas.count_documents({"lido": False})
    obrigacoes = await db.obrigacoes_empresa.count_documents({"status": "pendente"})

    return {
        "empresas": empresas,
        "alertas": alertas,
        "obrigacoes_pendentes": obrigacoes
    }
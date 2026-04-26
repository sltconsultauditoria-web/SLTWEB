"""
Router de Auditorias - /api/auditoria
Endpoints para auditoria fiscal no MongoDB (consultslt_db.auditorias)
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Auditoria"])


class AuditoriaCreate(BaseModel):
    cnpj: Optional[str] = None
    empresa_id: Optional[str] = None
    periodo: Optional[str] = None
    tipo: str = "sped_fiscal"
    status: str = "pendente"
    resultado: Optional[Any] = None


class AuditoriaUpdate(BaseModel):
    status: Optional[str] = None
    resultado: Optional[Any] = None


class AuditoriaResponse(BaseModel):
    id: str
    cnpj: Optional[str] = None
    empresa_id: Optional[str] = None
    periodo: Optional[str] = None
    tipo: str
    status: str
    resultado: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


def _s(doc):
    doc["id"] = str(doc.get("_id", doc.get("id", "")))
    doc.pop("_id", None)
    return doc


@router.get("/", response_model=List[AuditoriaResponse])
async def listar_auditorias(
    empresa_id: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Lista auditorias com filtros."""
    filtro = {}
    if empresa_id:
        filtro["empresa_id"] = empresa_id
    if status:
        filtro["status"] = status
    try:
        items = await db["auditorias"].find(filtro).to_list(100)
        return [_s(i) for i in items]
    except Exception as e:
        logger.error(f"Erro ao listar auditorias: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")


@router.get("/estatisticas")
async def get_estatisticas(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Retorna estatisticas das auditorias."""
    try:
        total = await db["auditorias"].count_documents({})
        concluidas = await db["auditorias"].count_documents({"status": "concluida"})
        pendentes = await db["auditorias"].count_documents({"status": "pendente"})
        erros = await db["auditorias"].count_documents({"status": "erro"})
        return {
            "total_auditorias": total,
            "concluidas": concluidas,
            "pendentes": pendentes,
            "erros": erros
        }
    except Exception as e:
        logger.error(f"Erro ao obter estatisticas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatisticas: {e}")


@router.post("/executar", status_code=202)
async def executar_auditoria(
    cnpj: str = Form(...),
    periodo: str = Form(...),
    tipo: str = Form(default="sped_fiscal"),
    empresa_id: Optional[str] = Form(default=None),
    arquivo: Optional[UploadFile] = File(default=None),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Submete uma auditoria para execucao."""
    doc = {
        "id": str(uuid.uuid4()),
        "cnpj": cnpj,
        "empresa_id": empresa_id,
        "periodo": periodo,
        "tipo": tipo,
        "status": "processando",
        "resultado": None,
        "created_at": datetime.utcnow(),
        "updated_at": None
    }
    await db["auditorias"].insert_one(doc)
    doc.pop("_id", None)
    return {"success": True, "auditoria_id": doc["id"], "status": "processando",
            "message": "Auditoria submetida para processamento"}


@router.post("/", response_model=AuditoriaResponse, status_code=201)
async def criar_auditoria(
    item: AuditoriaCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Cria uma nova auditoria."""
    doc = item.dict()
    doc["id"] = str(uuid.uuid4())
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = None
    await db["auditorias"].insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.get("/{item_id}", response_model=AuditoriaResponse)
async def obter_auditoria(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtém auditoria por ID."""
    item = await db["auditorias"].find_one({"id": item_id})
    if not item:
        raise HTTPException(status_code=404, detail="Auditoria nao encontrada")
    return _s(item)


@router.put("/{item_id}", response_model=AuditoriaResponse)
async def atualizar_auditoria(
    item_id: str,
    item: AuditoriaUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualiza uma auditoria."""
    u = item.dict(exclude_unset=True)
    u["updated_at"] = datetime.utcnow()
    r = await db["auditorias"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0:
        raise HTTPException(status_code=404, detail="Auditoria nao encontrada")
    return _s(await db["auditorias"].find_one({"id": item_id}))


@router.delete("/{item_id}")
async def deletar_auditoria(
    item_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Remove uma auditoria."""
    r = await db["auditorias"].delete_one({"id": item_id})
    if r.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Auditoria nao encontrada")
    return {"success": True}

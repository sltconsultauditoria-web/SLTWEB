"""
Router de Alertas - /api/alertas
CRUD completo para alertas no MongoDB (consultslt_db.alertas)
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Alertas"])


# ============================================================
# Schemas
# ============================================================
class AlertaCreate(BaseModel):
    tipo: str = Field(..., description="vencimento|obrigacao|certidao|documento|sistema|outro")
    prioridade: str = Field(default="media", description="baixa|media|alta|urgente")
    titulo: str
    mensagem: str
    empresa_id: Optional[str] = None
    entidade_tipo: Optional[str] = None
    entidade_id: Optional[str] = None


class AlertaUpdate(BaseModel):
    status: Optional[str] = None
    prioridade: Optional[str] = None
    observacoes: Optional[str] = None


class AlertaResponse(BaseModel):
    id: str
    titulo: str
    mensagem: str
    tipo: str
    severidade: str
    prioridade: Optional[str]
    lido: bool
    empresa_id: Optional[str]
    criado_em: str
    atualizado_em: Optional[str]

    @classmethod
    def from_db(cls, doc):
        return cls(
            id=doc.get("id"),
            titulo=doc.get("titulo"),
            mensagem=doc.get("mensagem"),
            tipo=doc.get("tipo"),
            severidade=doc.get("severidade", "unknown"),  # Default to "unknown" if None
            prioridade=doc.get("prioridade"),
            lido=doc.get("lido", False),  # Default to False if None
            empresa_id=doc.get("empresa_id"),
            criado_em=doc["created_at"].isoformat() if doc.get("created_at") else None,
            atualizado_em=doc["updated_at"].isoformat() if doc.get("updated_at") else None,
        )

def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.get("_id", doc.get("id", "")))
    doc.pop("_id", None)
    return doc


# ============================================================
# Endpoints
# ============================================================
@router.get("/", response_model=List[AlertaResponse])
async def listar_alertas(
    tipo: Optional[str] = Query(default=None),
    status: Optional[str] = Query(default=None),
    prioridade: Optional[str] = Query(default=None),
    empresa_id: Optional[str] = Query(default=None),
    pagina: int = Query(default=1, ge=1),
    por_pagina: int = Query(default=20, ge=1, le=100),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Lista alertas com filtros e paginação."""
    filtro = {}
    if tipo:
        filtro["tipo"] = tipo
    if status:
        filtro["status"] = status
    if prioridade:
        filtro["prioridade"] = prioridade
    if empresa_id:
        filtro["empresa_id"] = empresa_id

    skip = (pagina - 1) * por_pagina
    items = await db["alertas"].find(filtro).skip(skip).limit(por_pagina).to_list(por_pagina)
    return [AlertaResponse.from_db(i) for i in items]


@router.post("/", response_model=AlertaResponse, status_code=201)
async def criar_alerta(
    item: AlertaCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Cria um novo alerta."""
    doc = item.dict()
    doc["id"] = str(uuid.uuid4())
    doc["status"] = "pendente"
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()

    await db["alertas"].insert_one(doc)
    doc.pop("_id", None)
    return doc


@router.get("/{alerta_id}", response_model=AlertaResponse)
async def obter_alerta(
    alerta_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtém alerta por ID."""
    item = await db["alertas"].find_one({"id": alerta_id})
    if not item:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return _serialize(item)


@router.put("/{alerta_id}", response_model=AlertaResponse)
async def atualizar_alerta(
    alerta_id: str,
    item: AlertaUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualiza um alerta."""
    update_data = item.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    update_data["updated_at"] = datetime.utcnow()

    if update_data.get("status") == "lido":
        update_data["lido_em"] = datetime.utcnow()
    elif update_data.get("status") == "resolvido":
        update_data["resolvido_em"] = datetime.utcnow()

    result = await db["alertas"].update_one({"id": alerta_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")

    updated = await db["alertas"].find_one({"id": alerta_id})
    return _serialize(updated)


@router.delete("/{alerta_id}")
async def deletar_alerta(
    alerta_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Remove um alerta."""
    result = await db["alertas"].delete_one({"id": alerta_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Alerta não encontrado")
    return {"success": True, "message": "Alerta removido"}


class MarcarLidoRequest(BaseModel):
    ids: List[str]

@router.post("/marcar-como-lido")
async def marcar_como_lido(
    body: MarcarLidoRequest,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Marca alertas como lidos. Aceita: {"ids": ["id1","id2"]}"""
    result = await db["alertas"].update_many(
        {"id": {"$in": body.ids}},
        {"$set": {"status": "lido", "lido_em": datetime.utcnow(), "updated_at": datetime.utcnow()}}
    )
    return {"success": True, "message": f"{result.modified_count} alertas marcados como lidos"}


# Adicionando endpoints de configuração de alertas (SMTP, Twilio, Teams)
class SmtpConfig(BaseModel):
    host: str
    port: int = 587
    username: str
    password: str
    from_email: str

class TwilioConfig(BaseModel):
    account_sid: str
    auth_token: str
    from_number: str

class TeamsConfig(BaseModel):
    webhook_url: str
    channel_name: str = ""

class RecipientCreate(BaseModel):
    name: str
    email: Optional[str] = None
    whatsapp: Optional[str] = None
    notify_email: bool = True
    notify_whatsapp: bool = False
    notify_teams: bool = True
    threshold_levels: List[str] = ["critico", "alto"]

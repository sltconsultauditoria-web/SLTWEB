"""Router de Guias - /api/guias"""
import logging, uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter( tags=["Guias"])

class GuiaCreate(BaseModel):
    empresa: str
    empresa_id: Optional[str] = None
    tipo: str  # DAS, DARF, GPS, etc.
    competencia: str
    vencimento: Optional[str] = None
    valor: Optional[float] = None
    status: str = "pendente"
    codigo_barras: Optional[str] = None
    observacoes: Optional[str] = None

class GuiaUpdate(BaseModel):
    status: Optional[str] = None
    valor: Optional[float] = None
    codigo_barras: Optional[str] = None
    observacoes: Optional[str] = None

class GuiaResponse(BaseModel):
    id: str
    tipo: str
    competencia: str
    vencimento: str
    valor: float
    status: str
    empresa: Optional[str]
    criado_em: str
    atualizado_em: Optional[str]

    @classmethod
    def from_db(cls, doc):
        return cls(
            id=doc.get("id"),
            tipo=doc.get("tipo"),
            competencia=doc.get("competencia"),
            vencimento=doc["vencimento"].isoformat() if doc.get("vencimento") else None,
            valor=doc.get("valor"),
            status=doc.get("status"),
            empresa=doc.get("empresa"),
            criado_em=doc["created_at"].isoformat() if doc.get("created_at") else None,
            atualizado_em=doc["updated_at"].isoformat() if doc.get("updated_at") else None,
        )

def _s(doc): doc["id"] = str(doc.get("_id", doc.get("id",""))); doc.pop("_id",None); return doc

@router.get("/", response_model=List[GuiaResponse])
async def listar(db: AsyncIOMotorDatabase = Depends(get_db)):
    items = await db["guias"].find().to_list(200)
    return [GuiaResponse.from_db(i) for i in items]

@router.post("/", response_model=GuiaResponse, status_code=201)
async def criar(item: GuiaCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = item.dict(); doc["id"] = str(uuid.uuid4()); doc["created_at"] = datetime.utcnow()
    await db["guias"].insert_one(doc); doc.pop("_id",None); return doc

@router.get("/{item_id}", response_model=GuiaResponse)
async def obter(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["guias"].find_one({"id": item_id})
    if not item: raise HTTPException(404, "Guia não encontrada")
    return _s(item)

@router.put("/{item_id}", response_model=GuiaResponse)
async def atualizar(item_id: str, item: GuiaUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    u = item.dict(exclude_unset=True); u["updated_at"] = datetime.utcnow()
    r = await db["guias"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0: raise HTTPException(404, "Guia não encontrada")
    return _s(await db["guias"].find_one({"id": item_id}))

@router.delete("/{item_id}")
async def deletar(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    r = await db["guias"].delete_one({"id": item_id})
    if r.deleted_count == 0: raise HTTPException(404, "Guia não encontrada")
    return {"success": True}

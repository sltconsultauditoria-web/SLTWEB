"""Router de Débitos - /api/debitos"""
import logging, uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter( tags=["Débitos"])

class DebitoCreate(BaseModel):
    empresa: str
    empresa_id: Optional[str] = None
    tipo: str  # IRPJ, CSLL, PIS, COFINS, etc.
    competencia: Optional[str] = None
    valor: Optional[float] = None
    multa: Optional[float] = None
    juros: Optional[float] = None
    total: Optional[float] = None
    status: str = "em_aberto"  # em_aberto|parcelado|pago
    vencimento: Optional[str] = None
    numero_processo: Optional[str] = None

class DebitoUpdate(BaseModel):
    status: Optional[str] = None
    valor: Optional[float] = None
    multa: Optional[float] = None
    juros: Optional[float] = None
    total: Optional[float] = None
    numero_processo: Optional[str] = None

class DebitoResponse(DebitoCreate):
    id: str
    created_at: Optional[datetime] = None
    class Config: from_attributes = True

def _s(doc): doc["id"] = str(doc.get("_id", doc.get("id",""))); doc.pop("_id",None); return doc

@router.get("/", response_model=List[DebitoResponse])
async def listar(db: AsyncIOMotorDatabase = Depends(get_db)):
    return [_s(i) for i in await db["debitos"].find().to_list(200)]

@router.post("/", response_model=DebitoResponse, status_code=201)
async def criar(item: DebitoCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = item.dict(); doc["id"] = str(uuid.uuid4()); doc["created_at"] = datetime.utcnow()
    await db["debitos"].insert_one(doc); doc.pop("_id",None); return doc

@router.get("/{item_id}", response_model=DebitoResponse)
async def obter(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["debitos"].find_one({"id": item_id})
    if not item: raise HTTPException(404, "Débito não encontrado")
    return _s(item)

@router.put("/{item_id}", response_model=DebitoResponse)
async def atualizar(item_id: str, item: DebitoUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    u = item.dict(exclude_unset=True); u["updated_at"] = datetime.utcnow()
    r = await db["debitos"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0: raise HTTPException(404, "Débito não encontrado")
    return _s(await db["debitos"].find_one({"id": item_id}))

@router.delete("/{item_id}")
async def deletar(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    r = await db["debitos"].delete_one({"id": item_id})
    if r.deleted_count == 0: raise HTTPException(404, "Débito não encontrado")
    return {"success": True}

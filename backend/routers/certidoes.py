"""Router de Certidões - /api/certidoes"""
import logging, uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter( tags=["Certidões"])

class CertidaoCreate(BaseModel):
    empresa: str
    empresa_id: Optional[str] = None
    tipo: str  # FGTS, Receita Federal, Estadual, Municipal
    numero: Optional[str] = None
    data_emissao: Optional[str] = None
    data_validade: Optional[str] = None
    status: str = "valida"  # valida|vencida|pendente
    url: Optional[str] = None

class CertidaoUpdate(BaseModel):
    status: Optional[str] = None
    numero: Optional[str] = None
    data_emissao: Optional[str] = None
    data_validade: Optional[str] = None
    url: Optional[str] = None

class CertidaoResponse(CertidaoCreate):
    id: str
    created_at: Optional[datetime] = None
    class Config: from_attributes = True

def _s(doc): doc["id"] = str(doc.get("_id", doc.get("id",""))); doc.pop("_id",None); return doc

@router.get("/", response_model=List[CertidaoResponse])
async def listar(db: AsyncIOMotorDatabase = Depends(get_db)):
    return [_s(i) for i in await db["certidoes"].find().to_list(200)]

@router.post("/", response_model=CertidaoResponse, status_code=201)
async def criar(item: CertidaoCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = item.dict(); doc["id"] = str(uuid.uuid4()); doc["created_at"] = datetime.utcnow()
    await db["certidoes"].insert_one(doc); doc.pop("_id",None); return doc

@router.get("/{item_id}", response_model=CertidaoResponse)
async def obter(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["certidoes"].find_one({"id": item_id})
    if not item: raise HTTPException(404, "Certidão não encontrada")
    return _s(item)

@router.put("/{item_id}", response_model=CertidaoResponse)
async def atualizar(item_id: str, item: CertidaoUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    u = item.dict(exclude_unset=True); u["updated_at"] = datetime.utcnow()
    r = await db["certidoes"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0: raise HTTPException(404, "Certidão não encontrada")
    return _s(await db["certidoes"].find_one({"id": item_id}))

@router.delete("/{item_id}")
async def deletar(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    r = await db["certidoes"].delete_one({"id": item_id})
    if r.deleted_count == 0: raise HTTPException(404, "Certidão não encontrada")
    return {"success": True}

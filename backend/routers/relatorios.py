"""Router de Relatórios - /api/relatorios"""
import logging, uuid
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter( tags=["Relatórios"])

class RelatorioCreate(BaseModel):
    titulo: str
    tipo: str  # fiscal, contabil, gerencial, etc.
    empresa_id: Optional[str] = None
    periodo: Optional[str] = None
    dados: Optional[Any] = None
    ativo: bool = True

class RelatorioUpdate(BaseModel):
    titulo: Optional[str] = None
    dados: Optional[Any] = None
    ativo: Optional[bool] = None

class RelatorioResponse(RelatorioCreate):
    id: str
    created_at: Optional[datetime] = None
    class Config: from_attributes = True

def _s(doc): doc["id"] = str(doc.get("_id", doc.get("id",""))); doc.pop("_id",None); return doc

@router.get("/", response_model=List[RelatorioResponse])
async def listar(db: AsyncIOMotorDatabase = Depends(get_db)):
    return [_s(i) for i in await db["relatorios"].find().to_list(100)]

@router.post("/", response_model=RelatorioResponse, status_code=201)
async def criar(item: RelatorioCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = item.dict(); doc["id"] = str(uuid.uuid4()); doc["created_at"] = datetime.utcnow()
    await db["relatorios"].insert_one(doc); doc.pop("_id",None); return doc

@router.get("/{item_id}", response_model=RelatorioResponse)
async def obter(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["relatorios"].find_one({"id": item_id})
    if not item: raise HTTPException(404, "Relatório não encontrado")
    return _s(item)

@router.put("/{item_id}", response_model=RelatorioResponse)
async def atualizar(item_id: str, item: RelatorioUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    u = item.dict(exclude_unset=True); u["updated_at"] = datetime.utcnow()
    r = await db["relatorios"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0: raise HTTPException(404, "Relatório não encontrado")
    return _s(await db["relatorios"].find_one({"id": item_id}))

@router.delete("/{item_id}")
async def deletar(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    r = await db["relatorios"].delete_one({"id": item_id})
    if r.deleted_count == 0: raise HTTPException(404, "Relatório não encontrado")
    return {"success": True}

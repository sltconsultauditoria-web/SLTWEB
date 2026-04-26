"""Router de Configurações - /api/configuracoes"""
import logging, uuid
from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter( tags=["Configurações"])

class ConfiguracaoCreate(BaseModel):
    chave: str
    valor: Optional[Any] = None
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    ativo: bool = True

class ConfiguracaoUpdate(BaseModel):
    valor: Optional[Any] = None
    descricao: Optional[str] = None
    ativo: Optional[bool] = None

class ConfiguracaoResponse(ConfiguracaoCreate):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    class Config: from_attributes = True

def _s(doc): doc["id"] = str(doc.get("_id", doc.get("id",""))); doc.pop("_id",None); return doc

@router.get("/", response_model=List[ConfiguracaoResponse])
async def listar(categoria: Optional[str] = None, db: AsyncIOMotorDatabase = Depends(get_db)):
    filtro = {"categoria": categoria} if categoria else {}
    return [_s(i) for i in await db["configuracoes"].find(filtro).to_list(100)]

@router.post("/", response_model=ConfiguracaoResponse, status_code=201)
async def criar(item: ConfiguracaoCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    existe = await db["configuracoes"].find_one({"chave": item.chave})
    if existe: raise HTTPException(400, "Chave já existe")
    doc = item.dict(); doc["id"] = str(uuid.uuid4()); doc["created_at"] = datetime.utcnow(); doc["updated_at"] = None
    await db["configuracoes"].insert_one(doc); doc.pop("_id",None); return doc

@router.get("/chave/{chave}", response_model=ConfiguracaoResponse)
async def obter_por_chave(chave: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["configuracoes"].find_one({"chave": chave})
    if not item: raise HTTPException(404, "Configuração não encontrada")
    return _s(item)

@router.get("/{item_id}", response_model=ConfiguracaoResponse)
async def obter(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["configuracoes"].find_one({"id": item_id})
    if not item: raise HTTPException(404, "Configuração não encontrada")
    return _s(item)

@router.put("/{item_id}", response_model=ConfiguracaoResponse)
async def atualizar(item_id: str, item: ConfiguracaoUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    u = item.dict(exclude_unset=True); u["updated_at"] = datetime.utcnow()
    r = await db["configuracoes"].update_one({"id": item_id}, {"$set": u})
    if r.matched_count == 0: raise HTTPException(404, "Configuração não encontrada")
    return _s(await db["configuracoes"].find_one({"id": item_id}))

@router.delete("/{item_id}")
async def deletar(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    r = await db["configuracoes"].delete_one({"id": item_id})
    if r.deleted_count == 0: raise HTTPException(404, "Configuração não encontrada")
    return {"success": True}

"""
Router de Empresas - /api/empresas
CRUD completo para gestao de empresas no MongoDB (consultslt_db.empresas)
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.core.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Empresas"])


class EmpresaCreate(BaseModel):
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    regime_tributario: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    ativo: bool = True


class EmpresaUpdate(BaseModel):
    cnpj: Optional[str] = None
    razao_social: Optional[str] = None
    nome_fantasia: Optional[str] = None
    regime_tributario: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    ativo: Optional[bool] = None


class EmpresaResponse(BaseModel):
    id: str
    cnpj: str
    razao_social: str
    nome_fantasia: Optional[str] = None
    regime_tributario: Optional[str] = None
    inscricao_estadual: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    endereco: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    ativo: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


def _serialize(doc: dict) -> dict:
    """Converte documento MongoDB para dict com id string."""
    if "_id" in doc:
        # Se nao tem campo id proprio, usa o _id do MongoDB
        if "id" not in doc or not doc["id"]:
            doc["id"] = str(doc["_id"])
        doc.pop("_id")
    return doc


@router.get("/", response_model=List[EmpresaResponse])
async def listar_empresas(
    ativo: Optional[bool] = None,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Lista todas as empresas."""
    filtro = {}
    if ativo is not None:
        filtro["ativo"] = ativo
    try:
        items = await db["empresas"].find(filtro).to_list(200)
        return [_serialize(i) for i in items]
    except Exception as e:
        logger.error(f"Erro ao listar empresas: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")


@router.post("/", response_model=EmpresaResponse, status_code=201)
async def criar_empresa(
    item: EmpresaCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Cria uma nova empresa."""
    cnpj_limpo = "".join(filter(str.isdigit, item.cnpj))
    existing = await db["empresas"].find_one({"cnpj": cnpj_limpo})
    if existing:
        raise HTTPException(status_code=400, detail="CNPJ ja cadastrado.")

    item_dict = item.dict()
    item_dict["cnpj"] = cnpj_limpo
    item_dict["id"] = str(uuid.uuid4())
    item_dict["created_at"] = datetime.utcnow()
    item_dict["updated_at"] = None

    result = await db["empresas"].insert_one(item_dict)
    item_dict.pop("_id", None)
    return item_dict


@router.get("/{empresa_id}", response_model=EmpresaResponse)
async def obter_empresa(
    empresa_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtém empresa por ID."""
    item = await db["empresas"].find_one({"id": empresa_id})
    if not item:
        raise HTTPException(status_code=404, detail="Empresa nao encontrada")
    return _serialize(item)


@router.put("/{empresa_id}", response_model=EmpresaResponse)
async def atualizar_empresa(
    empresa_id: str,
    item: EmpresaUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualiza uma empresa."""
    update_data = item.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")

    update_data["updated_at"] = datetime.utcnow()
    result = await db["empresas"].update_one({"id": empresa_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Empresa nao encontrada")

    updated = await db["empresas"].find_one({"id": empresa_id})
    return _serialize(updated)


@router.delete("/{empresa_id}")
async def deletar_empresa(
    empresa_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Remove uma empresa (soft delete: ativo=False)."""
    result = await db["empresas"].update_one(
        {"id": empresa_id},
        {"$set": {"ativo": False, "updated_at": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Empresa nao encontrada")
    return {"success": True, "message": "Empresa desativada com sucesso"}

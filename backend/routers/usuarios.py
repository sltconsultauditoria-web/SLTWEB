"""
Router de Usuários - /api/usuarios
CRUD completo para gestão de usuários no MongoDB (consultslt_db.usuarios)
"""
import logging
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.core.database import get_db
from backend.auth_utils import hash_password

logger = logging.getLogger(__name__)

router = APIRouter( tags=["Usuários"])


# ============================================================
# Schemas
# ============================================================
class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    perfil: str = "user"  # super_admin | admin | user
    ativo: bool = True


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    perfil: Optional[str] = None
    ativo: Optional[bool] = None
    senha: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: str
    nome: str
    email: str
    perfil: str
    ativo: bool
    permissoes: List[str] = []
    criado_em: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioListResponse(BaseModel):
    usuarios: List[UsuarioResponse]
    total: int


PERMISSOES_POR_PERFIL = {
    "super_admin": ["read", "write", "delete", "admin"],
    "admin": ["read", "write", "delete"],
    "user": ["read"],
}


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.get("_id", doc.get("id", "")))
    doc.pop("_id", None)
    doc.pop("senha_hash", None)
    doc.pop("hashed_password", None)
    return doc


# ============================================================
# Endpoints
# ============================================================
@router.get("/", response_model=UsuarioListResponse)
async def listar_usuarios(
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Lista todos os usuários."""
    try:
        items = await db["usuarios"].find().to_list(200)
        usuarios = [_serialize(i) for i in items]
        return {"usuarios": usuarios, "total": len(usuarios)}
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {e}")


@router.post("/", response_model=UsuarioResponse, status_code=201)
async def criar_usuario(
    item: UsuarioCreate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Cria um novo usuário."""
    existing = await db["usuarios"].find_one({"email": item.email})
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")

    permissoes = PERMISSOES_POR_PERFIL.get(item.perfil, ["read"])

    novo = {
        "id": str(uuid.uuid4()),
        "nome": item.nome,
        "email": item.email,
        "senha_hash": hash_password(item.senha),
        "perfil": item.perfil,
        "permissoes": permissoes,
        "ativo": item.ativo,
        "primeiro_login": True,
        "criado_em": datetime.utcnow(),
        "atualizado_em": datetime.utcnow(),
    }

    await db["usuarios"].insert_one(novo)
    novo.pop("_id", None)
    return _serialize(novo)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obter_usuario(
    usuario_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Obtém usuário por ID."""
    item = await db["usuarios"].find_one({"id": usuario_id})
    if not item:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return _serialize(item)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def atualizar_usuario(
    usuario_id: str,
    item: UsuarioUpdate,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Atualiza um usuário."""
    update_data = item.dict(exclude_unset=True)

    if "senha" in update_data:
        update_data["senha_hash"] = hash_password(update_data.pop("senha"))

    if "perfil" in update_data:
        update_data["permissoes"] = PERMISSOES_POR_PERFIL.get(update_data["perfil"], ["read"])

    update_data["atualizado_em"] = datetime.utcnow()

    result = await db["usuarios"].update_one({"id": usuario_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    updated = await db["usuarios"].find_one({"id": usuario_id})
    return _serialize(updated)


@router.delete("/{usuario_id}")
async def deletar_usuario(
    usuario_id: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Desativa um usuário (soft delete)."""
    result = await db["usuarios"].update_one(
        {"id": usuario_id},
        {"$set": {"ativo": False, "atualizado_em": datetime.utcnow()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"success": True, "message": "Usuário desativado"}

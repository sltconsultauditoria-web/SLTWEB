from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.security import get_password_hash


router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])
db = get_db()


class UsuarioCreate(BaseModel):
    email: str
    nome: str | None = None
    password: str | None = None
    senha: str | None = None
    role: str = "user"
    ativo: bool = True


class UsuarioUpdate(BaseModel):
    email: str | None = None
    nome: str | None = None
    password: str | None = None
    senha: str | None = None
    role: str | None = None
    ativo: bool | None = None


def serialize(usuario):
    usuario["id"] = str(usuario.pop("_id"))
    usuario.pop("senha", None)
    usuario.pop("password", None)
    usuario.pop("hashed_password", None)
    usuario.pop("senha_hash", None)
    return usuario


@router.get("/")
async def list_usuarios():
    items = await db["usuarios"].find({"ativo": {"$ne": False}}).to_list(100)
    return [serialize(item) for item in items]


@router.post("/")
async def create_usuario(payload: UsuarioCreate):
    data = payload.dict(exclude_none=True)
    password = data.pop("password", None) or data.pop("senha", None)
    if password:
        data["senha_hash"] = get_password_hash(password)
    result = await db["usuarios"].insert_one(data)
    item = await db["usuarios"].find_one({"_id": result.inserted_id})
    return serialize(item)


@router.get("/{item_id}")
async def get_usuario(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    item = await db["usuarios"].find_one({"_id": ObjectId(item_id), "ativo": {"$ne": False}})
    if not item:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return serialize(item)


@router.put("/{item_id}")
async def update_usuario(item_id: str, payload: UsuarioUpdate):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    data = payload.dict(exclude_none=True)
    password = data.pop("password", None) or data.pop("senha", None)
    if password:
        data["senha_hash"] = get_password_hash(password)
    result = await db["usuarios"].update_one({"_id": ObjectId(item_id)}, {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    item = await db["usuarios"].find_one({"_id": ObjectId(item_id)})
    return serialize(item)


@router.delete("/{item_id}")
async def delete_usuario(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    result = await db["usuarios"].update_one({"_id": ObjectId(item_id)}, {"$set": {"ativo": False}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return {"deleted": 1}

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from backend.core.database import get_db
from backend.core.security import decode_access_token, get_password_hash


router = APIRouter(prefix="/api/usuarios", tags=["usuarios"])
db = get_db()
security = HTTPBearer()


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


def require_admin(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido")
    role = str(payload.get("role") or payload.get("perfil") or "").strip().lower()
    if role not in {"admin", "super_admin"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return payload


def serialize(usuario):
    usuario["id"] = str(usuario.pop("_id"))
    usuario.pop("senha", None)
    usuario.pop("password", None)
    usuario.pop("hashed_password", None)
    usuario.pop("senha_hash", None)
    return usuario


def is_viewer_role(role: str | None) -> bool:
    return str(role or "").strip().lower() == "viewer"


def object_query(item_id: str) -> dict:
    if ObjectId.is_valid(item_id):
        return {"_id": ObjectId(item_id)}
    return {"id": item_id}


@router.get("/")
async def list_usuarios(_current_user: dict = Depends(require_admin)):
    items = await db["usuarios"].find({"ativo": {"$ne": False}}).to_list(100)
    return [serialize(item) for item in items]


@router.post("/")
async def create_usuario(payload: UsuarioCreate, _current_user: dict = Depends(require_admin)):
    data = payload.dict(exclude_none=True)
    password = data.pop("password", None) or data.pop("senha", None)
    if password:
        data["senha_hash"] = get_password_hash(password)
    result = await db["usuarios"].insert_one(data)
    item = await db["usuarios"].find_one({"_id": result.inserted_id})
    return serialize(item)


@router.get("/viewers")
async def list_viewers(_current_user: dict = Depends(require_admin)):
    items = await db["usuarios"].find({"ativo": {"$ne": False}}).to_list(100)
    return [serialize(item) for item in items if is_viewer_role(item.get("role") or item.get("perfil"))]


@router.post("/viewers", status_code=status.HTTP_201_CREATED)
async def create_viewer(payload: UsuarioCreate, _current_user: dict = Depends(require_admin)):
    data = payload.dict(exclude_none=True)
    password = data.pop("password", None) or data.pop("senha", None)
    data["role"] = "viewer"
    data["perfil"] = "viewer"
    if password:
        data["senha_hash"] = get_password_hash(password)
    result = await db["usuarios"].insert_one(data)
    item = await db["usuarios"].find_one({"_id": result.inserted_id})
    return serialize(item)


@router.put("/viewers/{item_id}")
async def update_viewer(item_id: str, payload: UsuarioUpdate, _current_user: dict = Depends(require_admin)):
    existing = await db["usuarios"].find_one(object_query(item_id))
    if not existing:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if not is_viewer_role(existing.get("role") or existing.get("perfil")):
        raise HTTPException(status_code=409, detail="Endpoint restrito a usuarios viewer")
    data = payload.dict(exclude_none=True)
    password = data.pop("password", None) or data.pop("senha", None)
    data["role"] = "viewer"
    data["perfil"] = "viewer"
    if password:
        data["senha_hash"] = get_password_hash(password)
    result = await db["usuarios"].update_one(object_query(item_id), {"$set": data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    item = await db["usuarios"].find_one(object_query(item_id))
    return serialize(item)


@router.delete("/viewers/{item_id}")
async def delete_viewer(item_id: str, _current_user: dict = Depends(require_admin)):
    existing = await db["usuarios"].find_one(object_query(item_id))
    if not existing:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    if not is_viewer_role(existing.get("role") or existing.get("perfil")):
        raise HTTPException(status_code=409, detail="Endpoint restrito a usuarios viewer")
    result = await db["usuarios"].update_one(object_query(item_id), {"$set": {"ativo": False}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return {"deleted": 1}


@router.get("/{item_id}")
async def get_usuario(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    item = await db["usuarios"].find_one({"_id": ObjectId(item_id), "ativo": {"$ne": False}})
    if not item:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return serialize(item)


@router.put("/{item_id}")
async def update_usuario(item_id: str, payload: UsuarioUpdate, _current_user: dict = Depends(require_admin)):
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
async def delete_usuario(item_id: str, _current_user: dict = Depends(require_admin)):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    result = await db["usuarios"].update_one({"_id": ObjectId(item_id)}, {"$set": {"ativo": False}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return {"deleted": 1}

from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.core.database import get_db


router = APIRouter(prefix="/api/empresas", tags=["empresas"])
db = get_db()


class EmpresaPayload(BaseModel):
    data: dict = Field(default_factory=dict)
    ativo: bool | None = True

    class Config:
        extra = "allow"


def normalize(payload):
    raw = payload.dict(exclude_none=True)
    data = raw.pop("data", {}) or {}
    data.update(raw)
    if "razao_social" not in data:
        data["razao_social"] = data.get("nome") or data.get("nome_fantasia") or "Empresa sem nome"
    if "cnpj" not in data:
        data["cnpj"] = "00.000.000/0001-00"
    if "regime" not in data:
        data["regime"] = data.get("regime_tributario") or "Simples Nacional"
    data.setdefault("ativo", True)
    data["updated_at"] = datetime.utcnow()
    return data


def serialize(item):
    item["id"] = str(item.pop("_id"))
    item.setdefault("ativo", True)
    item["data"] = {k: v for k, v in item.items() if k not in {"id", "ativo"}}
    return item


@router.get("/")
async def list_items():
    items = await db["empresas"].find({"ativo": {"$ne": False}}).to_list(100)
    return [serialize(item) for item in items]


@router.post("/")
async def create_item(item: EmpresaPayload):
    data = normalize(item)
    data["created_at"] = datetime.utcnow()
    result = await db["empresas"].insert_one(data)
    created = await db["empresas"].find_one({"_id": result.inserted_id})
    return serialize(created)


@router.get("/{item_id}")
async def get_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    item = await db["empresas"].find_one({"_id": ObjectId(item_id), "ativo": {"$ne": False}})
    if not item:
        raise HTTPException(status_code=404, detail="Empresa nao encontrada")
    return serialize(item)


@router.put("/{item_id}")
async def update_item(item_id: str, item: EmpresaPayload):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    result = await db["empresas"].update_one({"_id": ObjectId(item_id)}, {"$set": normalize(item)})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Empresa nao encontrada")
    updated = await db["empresas"].find_one({"_id": ObjectId(item_id)})
    return serialize(updated)


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID invalido")
    result = await db["empresas"].update_one({"_id": ObjectId(item_id)}, {"$set": {"ativo": False}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Empresa nao encontrada")
    return {"deleted": 1}

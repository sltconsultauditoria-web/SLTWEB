from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.obrigacoes_schema import ObrigacoesCreate, ObrigacoesUpdate, ObrigacoesSchema, ObrigacaoListResponse
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/obrigacoes", tags=["obrigacoes"])

db = get_db()

@router.get("/", response_model=ObrigacaoListResponse)
async def list_items():
    items = await db["obrigacoes"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
        i["data"] = i.get("data", {})  # Adiciona o campo 'data' com valor padrão se não existir
        i.pop("_id", None)  # Remove o campo '_id' para evitar conflitos
    return {"data": items}

@router.post("/", response_model=ObrigacoesSchema)
async def create_item(item: ObrigacoesCreate):
    result = await db["obrigacoes"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=ObrigacoesSchema)
async def get_item(item_id: str):
    item = await db["obrigacoes"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=ObrigacoesSchema)
async def update_item(item_id: str, item: ObrigacoesUpdate):
    await db["obrigacoes"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["obrigacoes"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["obrigacoes"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

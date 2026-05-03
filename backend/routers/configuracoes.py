from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.configuracoes_schema import ConfiguracoesCreate, ConfiguracoesUpdate, ConfiguracoesSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/configuracoes", tags=["configuracoes"])

db = get_db()

@router.get("/", response_model=List[ConfiguracoesSchema])
async def list_items():
    items = await db["configuracoes"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=ConfiguracoesSchema)
async def create_item(item: ConfiguracoesCreate):
    result = await db["configuracoes"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=ConfiguracoesSchema)
async def get_item(item_id: str):
    item = await db["configuracoes"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=ConfiguracoesSchema)
async def update_item(item_id: str, item: ConfiguracoesUpdate):
    await db["configuracoes"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["configuracoes"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["configuracoes"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

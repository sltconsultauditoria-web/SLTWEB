from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.guias_schema import GuiasCreate, GuiasUpdate, GuiasSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/guias", tags=["guias"])

db = get_db()

@router.get("/", response_model=List[GuiasSchema])
async def list_items():
    items = await db["guias"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=GuiasSchema)
async def create_item(item: GuiasCreate):
    result = await db["guias"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=GuiasSchema)
async def get_item(item_id: str):
    item = await db["guias"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=GuiasSchema)
async def update_item(item_id: str, item: GuiasUpdate):
    await db["guias"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["guias"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["guias"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.health_check_schema import Health_checkCreate, Health_checkUpdate, Health_checkSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/health_check", tags=["health_check"])

db = get_db()

@router.get("/", response_model=List[Health_checkSchema])
async def list_items():
    items = await db["health_check"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=Health_checkSchema)
async def create_item(item: Health_checkCreate):
    result = await db["health_check"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=Health_checkSchema)
async def get_item(item_id: str):
    item = await db["health_check"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=Health_checkSchema)
async def update_item(item_id: str, item: Health_checkUpdate):
    await db["health_check"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["health_check"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["health_check"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

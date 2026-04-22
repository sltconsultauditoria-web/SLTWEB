from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.status_checks_schema import Status_checksCreate, Status_checksUpdate, Status_checksSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/status_checks", tags=["status_checks"])

db = get_db()

@router.get("/", response_model=List[Status_checksSchema])
async def list_items():
    items = await db["status_checks"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=Status_checksSchema)
async def create_item(item: Status_checksCreate):
    result = await db["status_checks"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=Status_checksSchema)
async def get_item(item_id: str):
    item = await db["status_checks"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=Status_checksSchema)
async def update_item(item_id: str, item: Status_checksUpdate):
    await db["status_checks"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["status_checks"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["status_checks"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

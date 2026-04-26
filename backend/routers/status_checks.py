from fastapi import APIRouter, HTTPException, Depends
from backend.core.database import get_db
from backend.schemas.status_checks_schema import Status_checksCreate, Status_checksUpdate, Status_checksSchema
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter( tags=["status_checks"])

@router.get("/", response_model=List[Status_checksSchema])
async def list_items(db: AsyncIOMotorDatabase = Depends(get_db)):
    items = await db["status_checks"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
        del i["_id"]
    return items

@router.post("/", response_model=Status_checksSchema)
async def create_item(item: Status_checksCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    item_dict = item.dict()
    item_dict["ativo"] = True
    result = await db["status_checks"].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return item_dict

@router.get("/{item_id}", response_model=Status_checksSchema)
async def get_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["status_checks"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    del item["_id"]
    return item

@router.put("/{item_id}", response_model=Status_checksSchema)
async def update_item(item_id: str, item: Status_checksUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    await db["status_checks"].update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict(exclude_unset=True)}
    )
    updated = await db["status_checks"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    del updated["_id"]
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["status_checks"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

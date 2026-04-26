from fastapi import APIRouter, HTTPException, Depends
from backend.core.database import get_db
from backend.schemas.fiscal_data_schema import Fiscal_dataCreate, Fiscal_dataUpdate, Fiscal_dataSchema
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter( tags=["fiscal_data"])

@router.get("/", response_model=List[Fiscal_dataSchema])
async def list_items(db: AsyncIOMotorDatabase = Depends(get_db)):
    items = await db["fiscal_data"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
        del i["_id"]
    return items

@router.post("/", response_model=Fiscal_dataSchema)
async def create_item(item: Fiscal_dataCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    item_dict = item.dict()
    item_dict["ativo"] = True
    result = await db["fiscal_data"].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return item_dict

@router.get("/{item_id}", response_model=Fiscal_dataSchema)
async def get_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["fiscal_data"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    del item["_id"]
    return item

@router.put("/{item_id}", response_model=Fiscal_dataSchema)
async def update_item(item_id: str, item: Fiscal_dataUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    await db["fiscal_data"].update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict(exclude_unset=True)}
    )
    updated = await db["fiscal_data"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    del updated["_id"]
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["fiscal_data"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

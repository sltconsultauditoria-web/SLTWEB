from fastapi import APIRouter, HTTPException, Depends
from backend.core.database import get_db
from backend.schemas.relatorios_gerados_schema import Relatorios_geradosCreate, Relatorios_geradosUpdate, Relatorios_geradosSchema
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter( tags=["relatorios_gerados"])

@router.get("/", response_model=List[Relatorios_geradosSchema])
async def list_items(db: AsyncIOMotorDatabase = Depends(get_db)):
    items = await db["relatorios_gerados"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
        del i["_id"]
    return items

@router.post("/", response_model=Relatorios_geradosSchema)
async def create_item(item: Relatorios_geradosCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    item_dict = item.dict()
    item_dict["ativo"] = True
    result = await db["relatorios_gerados"].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return item_dict

@router.get("/{item_id}", response_model=Relatorios_geradosSchema)
async def get_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["relatorios_gerados"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    del item["_id"]
    return item

@router.put("/{item_id}", response_model=Relatorios_geradosSchema)
async def update_item(item_id: str, item: Relatorios_geradosUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    await db["relatorios_gerados"].update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict(exclude_unset=True)}
    )
    updated = await db["relatorios_gerados"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    del updated["_id"]
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["relatorios_gerados"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

from fastapi import APIRouter, HTTPException, Depends
from backend.core.database import get_db
from backend.schemas.tipos_obrigacoes_schema import Tipos_obrigacoesCreate, Tipos_obrigacoesUpdate, Tipos_obrigacoesSchema
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter( tags=["tipos_obrigacoes"])

@router.get("/", response_model=List[Tipos_obrigacoesSchema])
async def list_items(db: AsyncIOMotorDatabase = Depends(get_db)):
    items = await db["tipos_obrigacoes"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
        del i["_id"]
    return items

@router.post("/", response_model=Tipos_obrigacoesSchema)
async def create_item(item: Tipos_obrigacoesCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    item_dict = item.dict()
    item_dict["ativo"] = True
    result = await db["tipos_obrigacoes"].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)
    return item_dict

@router.get("/{item_id}", response_model=Tipos_obrigacoesSchema)
async def get_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    item = await db["tipos_obrigacoes"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    del item["_id"]
    return item

@router.put("/{item_id}", response_model=Tipos_obrigacoesSchema)
async def update_item(item_id: str, item: Tipos_obrigacoesUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    await db["tipos_obrigacoes"].update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict(exclude_unset=True)}
    )
    updated = await db["tipos_obrigacoes"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    del updated["_id"]
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["tipos_obrigacoes"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

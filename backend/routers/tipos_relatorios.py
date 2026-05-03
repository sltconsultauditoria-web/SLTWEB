from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.tipos_relatorios_schema import Tipos_relatoriosCreate, Tipos_relatoriosUpdate, Tipos_relatoriosSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/tipos_relatorios", tags=["tipos_relatorios"])

db = get_db()

@router.get("/", response_model=List[Tipos_relatoriosSchema])
async def list_items():
    items = await db["tipos_relatorios"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=Tipos_relatoriosSchema)
async def create_item(item: Tipos_relatoriosCreate):
    result = await db["tipos_relatorios"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=Tipos_relatoriosSchema)
async def get_item(item_id: str):
    item = await db["tipos_relatorios"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=Tipos_relatoriosSchema)
async def update_item(item_id: str, item: Tipos_relatoriosUpdate):
    await db["tipos_relatorios"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["tipos_relatorios"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["tipos_relatorios"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

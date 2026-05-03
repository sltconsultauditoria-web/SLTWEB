from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.documentos_empresa_schema import Documentos_empresaCreate, Documentos_empresaUpdate, Documentos_empresaSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/documentos_empresa", tags=["documentos_empresa"])

db = get_db()

@router.get("/", response_model=List[Documentos_empresaSchema])
async def list_items():
    items = await db["documentos_empresa"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=Documentos_empresaSchema)
async def create_item(item: Documentos_empresaCreate):
    result = await db["documentos_empresa"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=Documentos_empresaSchema)
async def get_item(item_id: str):
    item = await db["documentos_empresa"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=Documentos_empresaSchema)
async def update_item(item_id: str, item: Documentos_empresaUpdate):
    await db["documentos_empresa"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["documentos_empresa"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["documentos_empresa"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

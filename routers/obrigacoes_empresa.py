from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.obrigacoes_empresa_schema import Obrigacoes_empresaCreate, Obrigacoes_empresaUpdate, Obrigacoes_empresaSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/obrigacoes_empresa", tags=["obrigacoes_empresa"])

db = get_db()

@router.get("/", response_model=List[Obrigacoes_empresaSchema])
async def list_items():
    items = await db["obrigacoes_empresa"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=Obrigacoes_empresaSchema)
async def create_item(item: Obrigacoes_empresaCreate):
    result = await db["obrigacoes_empresa"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=Obrigacoes_empresaSchema)
async def get_item(item_id: str):
    item = await db["obrigacoes_empresa"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=Obrigacoes_empresaSchema)
async def update_item(item_id: str, item: Obrigacoes_empresaUpdate):
    await db["obrigacoes_empresa"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["obrigacoes_empresa"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["obrigacoes_empresa"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

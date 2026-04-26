from fastapi import APIRouter, HTTPException
from backend.core.database import get_database
from backend.schemas.obrigacoes_empresa_schema import (
    Obrigacoes_empresaCreate,
    Obrigacoes_empresaUpdate,
    Obrigacoes_empresaSchema
)
from typing import List
from bson import ObjectId

router = APIRouter(tags=["Obrigacoes Empresa"])


@router.get("/", response_model=List[Obrigacoes_empresaSchema])
async def list_items():
    db = get_database()
    items = await db["obrigacoes_empresa"].find().to_list(100)

    for i in items:
        i["id"] = str(i["_id"])
        del i["_id"]

    return items


@router.post("/", response_model=Obrigacoes_empresaSchema)
async def create_item(item: Obrigacoes_empresaCreate):
    db = get_database()

    item_dict = item.dict()
    item_dict["ativo"] = True

    result = await db["obrigacoes_empresa"].insert_one(item_dict)
    item_dict["id"] = str(result.inserted_id)

    return item_dict


@router.get("/{item_id}", response_model=Obrigacoes_empresaSchema)
async def get_item(item_id: str):
    db = get_database()

    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    item = await db["obrigacoes_empresa"].find_one({"_id": ObjectId(item_id)})

    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    item["id"] = str(item["_id"])
    del item["_id"]

    return item


@router.put("/{item_id}", response_model=Obrigacoes_empresaSchema)
async def update_item(item_id: str, item: Obrigacoes_empresaUpdate):
    db = get_database()

    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    await db["obrigacoes_empresa"].update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item.dict(exclude_unset=True)}
    )

    updated = await db["obrigacoes_empresa"].find_one({"_id": ObjectId(item_id)})

    if not updated:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    updated["id"] = str(updated["_id"])
    del updated["_id"]

    return updated


@router.delete("/{item_id}")
async def delete_item(item_id: str):
    db = get_database()

    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await db["obrigacoes_empresa"].delete_one({"_id": ObjectId(item_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    return {"deleted": result.deleted_count}
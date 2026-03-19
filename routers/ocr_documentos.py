from fastapi import APIRouter, HTTPException
from backend.core.database import get_db
from backend.schemas.ocr_documentos_schema import Ocr_documentosCreate, Ocr_documentosUpdate, Ocr_documentosSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/ocr_documentos", tags=["ocr_documentos"])

db = get_db()

@router.get("/", response_model=List[Ocr_documentosSchema])
async def list_items():
    items = await db["ocr_documentos"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=Ocr_documentosSchema)
async def create_item(item: Ocr_documentosCreate):
    result = await db["ocr_documentos"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

@router.get("/{item_id}", response_model=Ocr_documentosSchema)
async def get_item(item_id: str):
    item = await db["ocr_documentos"].find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    item["id"] = str(item["_id"])
    return item

@router.put("/{item_id}", response_model=Ocr_documentosSchema)
async def update_item(item_id: str, item: Ocr_documentosUpdate):
    await db["ocr_documentos"].update_one({"_id": ObjectId(item_id)}, {"$set": item.dict(exclude_unset=True)})
    updated = await db["ocr_documentos"].find_one({"_id": ObjectId(item_id)})
    updated["id"] = str(updated["_id"])
    return updated

@router.delete("/{item_id}", response_model=dict)
async def delete_item(item_id: str):
    result = await db["ocr_documentos"].delete_one({"_id": ObjectId(item_id)})
    return {"deleted": result.deleted_count}

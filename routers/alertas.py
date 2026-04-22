from fastapi import APIRouter, HTTPException, Depends
from backend.core.database import get_db
from backend.schemas.alertas_schema import AlertasCreate, AlertasUpdate, AlertasSchema
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/api/alertas", tags=["alertas"])

async def get_db_dependency():
    return get_db()

@router.get("/", response_model=List[AlertasSchema])
async def list_items(db=Depends(get_db_dependency)):
    items = await db["alertas"].find().to_list(100)
    for i in items:
        i["id"] = str(i["_id"])
    return items

@router.post("/", response_model=AlertasSchema)
async def create_item(item: AlertasCreate, db=Depends(get_db_dependency)):
    result = await db["alertas"].insert_one(item.dict())
    item_dict = item.dict()
    item_dict["id"] = str(result.inserted_id)
    item_dict["ativo"] = True
    return item_dict

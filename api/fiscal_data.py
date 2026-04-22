from fastapi import APIRouter, HTTPException
from backend.schemas.fiscal_data import Fiscal_dataCreate
from backend.repositories.fiscal_data_repository import *

router = APIRouter(prefix="/fiscal_data", tags=["fiscal_data"])

@router.post("/")
def create_item(data: Fiscal_dataCreate):
    return {"id": create(data.model_dump())}

@router.get("/")
def list_items():
    return list_all()

@router.get("/{id}")
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(404, "fiscal_data not found")
    return item

@router.put("/{id}")
def update_item(id: str, data: Fiscal_dataCreate):
    return update(id, data.model_dump())

@router.delete("/{id}")
def delete_item(id: str):
    delete(id)
    return {"ok": True}
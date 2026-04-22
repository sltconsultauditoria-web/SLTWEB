from fastapi import APIRouter, HTTPException
from backend.schemas.certidoes_empresa import Certidoes_empresaCreate
from backend.repositories.certidoes_empresa_repository import *

router = APIRouter(prefix="/certidoes_empresa", tags=["certidoes_empresa"])

@router.post("/")
def create_item(data: Certidoes_empresaCreate):
    return {"id": create(data.model_dump())}

@router.get("/")
def list_items():
    return list_all()

@router.get("/{id}")
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(404, "certidoes_empresa not found")
    return item

@router.put("/{id}")
def update_item(id: str, data: Certidoes_empresaCreate):
    return update(id, data.model_dump())

@router.delete("/{id}")
def delete_item(id: str):
    delete(id)
    return {"ok": True}
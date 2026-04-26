from fastapi import APIRouter, HTTPException
from backend.certidoes_empresa import Certidoes_empresaCreate
from backend.repositories.certidoes_empresa_repository import *

router = APIRouter(prefix="/api/certidoes_empresa", tags=["Certidoes Empresa"])

@router.post("/")
def create_item(data: Certidoes_empresaCreate):
    return {"id": create(data.model_dump())}

@router.get("/")
def list_items():
    return mongo_list_to_dict_list(list_all())

@router.get("/{id}")
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(404, "certidoes_empresa not found")
    return mongo_list_to_dict_list([item])[0]

@router.put("/{id}")
def update_item(id: str, data: Certidoes_empresaCreate):
    updated_item = update(id, data.model_dump())
    return mongo_list_to_dict_list([updated_item])[0]

@router.delete("/{id}")
def delete_item(id: str):
    delete(id)
    return {"ok": True}
from fastapi import APIRouter, HTTPException
from backend.schemas.obrigacoes_empresa import Obrigacoes_empresaCreate
from backend.repositories.obrigacoes_empresa_repository import *

router = APIRouter(prefix="/obrigacoes_empresa", tags=["obrigacoes_empresa"])

@router.post("/")
def create_item(data: Obrigacoes_empresaCreate):
    return {"id": create(data.model_dump())}

@router.get("/")
def list_items():
    return list_all()

@router.get("/{id}")
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(404, "obrigacoes_empresa not found")
    return item

@router.put("/{id}")
def update_item(id: str, data: Obrigacoes_empresaCreate):
    return update(id, data.model_dump())

@router.delete("/{id}")
def delete_item(id: str):
    delete(id)
    return {"ok": True}
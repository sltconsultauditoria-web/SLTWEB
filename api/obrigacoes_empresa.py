from fastapi import APIRouter, HTTPException
from typing import List

from backend.schemas.obrigacoes_empresa import (
    Obrigacoes_empresaCreate,
    Obrigacoes_empresaResponse
)
from backend.repositories.obrigacoes_empresa_repository import (
    create,
    list_all,
    get_by_id,
    update,
    delete
)

router = APIRouter(prefix="/obrigacoes_empresa", tags=["Obrigações Empresa"])


@router.post("/", response_model=Obrigacoes_empresaResponse)
def create_item(data: Obrigacoes_empresaCreate):
    item_id = create(data.model_dump())
    item = get_by_id(item_id)
    return item


@router.get("/", response_model=List[Obrigacoes_empresaResponse])
def list_items():
    return list_all()


@router.get("/{id}", response_model=Obrigacoes_empresaResponse)
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Obrigação Empresa não encontrada")
    return item


@router.put("/{id}", response_model=Obrigacoes_empresaResponse)
def update_item(id: str, data: Obrigacoes_empresaCreate):
    updated = update(id, data.model_dump())
    if not updated:
        raise HTTPException(status_code=404, detail="Obrigação Empresa não encontrada")

    return get_by_id(id)


@router.delete("/{id}")
def delete_item(id: str):
    deleted = delete(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Obrigação Empresa não encontrada")

    return {"message": "Obrigação Empresa deletada com sucesso"}
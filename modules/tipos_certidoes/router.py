from fastapi import APIRouter
from .schemas import CreateSchema, UpdateSchema
from .service import criar, listar, obter, atualizar, remover

router = APIRouter(prefix="/tipos_certidoes", tags=["tipos_certidoes"])

@router.post("/")
def criar_item(data: CreateSchema):
    return criar(data.dict())

@router.get("/")
def listar_itens():
    return listar()

@router.get("/{id}")
def obter_item(id: str):
    return obter(id)

@router.put("/{id}")
def atualizar_item(id: str, data: UpdateSchema):
    return atualizar(id, data.dict(exclude_unset=True))

@router.delete("/{id}")
def remover_item(id: str):
    return remover(id)

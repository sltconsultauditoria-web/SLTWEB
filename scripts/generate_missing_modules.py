import os

BASE_PATH = "backend/modules"

collections = [
    "certidoes",
    "certidoes_empresa",
    "configuracoes",
    "debitos",
    "documentos_empresa",
    "guias",
    "obrigacoes",
    "obrigacoes_empresa",
    "ocr_documentos",
    "relatorios",
    "relatorios_gerados",
    "robots",
    "status_checks",
    "tipos_certidoes",
    "tipos_documentos",
    "tipos_obrigacoes",
    "tipos_relatorios"
]

schema_template = """from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    nome: Optional[str] = None
    ativo: bool = True
    criado_em: datetime | None = None

class CreateSchema(BaseSchema):
    pass

class UpdateSchema(BaseSchema):
    pass
"""

repository_template = """from backend.database import get_collection
from bson import ObjectId

collection = get_collection("{collection}")

def create(data: dict):
    return collection.insert_one(data)

def find_all():
    return list(collection.find())

def find_by_id(id: str):
    return collection.find_one({{"_id": ObjectId(id)}})

def update(id: str, data: dict):
    return collection.update_one(
        {{"_id": ObjectId(id)}},
        {{"$set": data}}
    )

def delete(id: str):
    return collection.delete_one({{"_id": ObjectId(id)}})
"""

service_template = """from .repository import create, find_all, find_by_id, update, delete

def criar(data: dict):
    return create(data)

def listar():
    return find_all()

def obter(id: str):
    return find_by_id(id)

def atualizar(id: str, data: dict):
    return update(id, data)

def remover(id: str):
    return delete(id)
"""

router_template = """from fastapi import APIRouter
from .schemas import CreateSchema, UpdateSchema
from .service import criar, listar, obter, atualizar, remover

router = APIRouter(prefix="/{collection}", tags=["{collection}"])

@router.post("/")
def criar_item(data: CreateSchema):
    return criar(data.dict())

@router.get("/")
def listar_itens():
    return listar()

@router.get("/{{id}}")
def obter_item(id: str):
    return obter(id)

@router.put("/{{id}}")
def atualizar_item(id: str, data: UpdateSchema):
    return atualizar(id, data.dict(exclude_unset=True))

@router.delete("/{{id}}")
def remover_item(id: str):
    return remover(id)
"""

for col in collections:
    path = os.path.join(BASE_PATH, col)
    os.makedirs(path, exist_ok=True)

    with open(f"{path}/schemas.py", "w", encoding="utf-8") as f:
        f.write(schema_template)

    with open(f"{path}/repository.py", "w", encoding="utf-8") as f:
        f.write(repository_template.format(collection=col))

    with open(f"{path}/service.py", "w", encoding="utf-8") as f:
        f.write(service_template)

    with open(f"{path}/router.py", "w", encoding="utf-8") as f:
        f.write(router_template.format(collection=col))

    with open(f"{path}/__init__.py", "w") as f:
        f.write("")

print("✅ Todos os módulos foram gerados com sucesso.")

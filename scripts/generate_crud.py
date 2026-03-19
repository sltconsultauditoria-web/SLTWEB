import os

collections = [
    "alertas",
    "certidoes",
    "certidoes_empresa",
    "configuracoes",
    "dashboard_metrics",
    "debitos",
    "documentos_empresa",
    "empresas",
    "fiscal",
    "fiscal_data",
    "guias",
    "obrigacoes",
    "obrigacoes_empresa",
]

BASE_PATH = os.path.dirname(os.path.dirname(__file__))

SCHEMA_PATH = os.path.join(BASE_PATH, "schemas")
REPO_PATH = os.path.join(BASE_PATH, "repositories")
ROUTER_PATH = os.path.join(BASE_PATH, "api")

os.makedirs(SCHEMA_PATH, exist_ok=True)
os.makedirs(REPO_PATH, exist_ok=True)
os.makedirs(ROUTER_PATH, exist_ok=True)


def create_schema(name):
    content = f"""
from pydantic import BaseModel
from typing import Optional

class {name.capitalize()}Base(BaseModel):
    nome: Optional[str] = None

class {name.capitalize()}Create({name.capitalize()}Base):
    pass

class {name.capitalize()}Response({name.capitalize()}Base):
    id: str
"""
    with open(os.path.join(SCHEMA_PATH, f"{name}.py"), "w") as f:
        f.write(content.strip())


def create_repository(name):
    content = f"""
from bson import ObjectId
from backend.core.database import get_collection

collection = get_collection("{name}")

def create(data: dict):
    result = collection.insert_one(data)
    return str(result.inserted_id)

def list_all():
    items = []
    for item in collection.find():
        item["id"] = str(item["_id"])
        del item["_id"]
        items.append(item)
    return items

def get_by_id(id: str):
    item = collection.find_one({{"_id": ObjectId(id)}})
    if not item:
        return None
    item["id"] = str(item["_id"])
    del item["_id"]
    return item

def update(id: str, data: dict):
    collection.update_one({{"_id": ObjectId(id)}}, {{"$set": data}})
    return get_by_id(id)

def delete(id: str):
    collection.delete_one({{"_id": ObjectId(id)}})
    return True
"""
    with open(os.path.join(REPO_PATH, f"{name}_repository.py"), "w") as f:
        f.write(content.strip())


def create_router(name):
    class_name = name.capitalize()

    content = f"""
from fastapi import APIRouter, HTTPException
from backend.schemas.{name} import {class_name}Create
from backend.repositories.{name}_repository import *

router = APIRouter(prefix="/{name}", tags=["{name}"])

@router.post("/")
def create_item(data: {class_name}Create):
    return {{"id": create(data.model_dump())}}

@router.get("/")
def list_items():
    return list_all()

@router.get("/{{id}}")
def get_item(id: str):
    item = get_by_id(id)
    if not item:
        raise HTTPException(404, "{name} not found")
    return item

@router.put("/{{id}}")
def update_item(id: str, data: {class_name}Create):
    return update(id, data.model_dump())

@router.delete("/{{id}}")
def delete_item(id: str):
    delete(id)
    return {{"ok": True}}
"""
    with open(os.path.join(ROUTER_PATH, f"{name}.py"), "w") as f:
        f.write(content.strip())


for collection in collections:
    create_schema(collection)
    create_repository(collection)
    create_router(collection)

print("✅ CRUDs gerados com sucesso.")

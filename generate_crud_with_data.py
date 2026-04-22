# generate_crud_with_data.py
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

ROUTERS_DIR = "backend/routers"
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

# Documento de teste genérico
TEST_DOC = {
    "nome": "Registro de Teste",
    "descricao": "Documento inserido automaticamente para validar integração",
    "ativo": True
}

TEMPLATE = """from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from backend.core.database import get_db

router = APIRouter()

def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
async def list_{name}(db: AsyncIOMotorDatabase = Depends(get_db)):
    docs = await db["{name}"].find().to_list(100)
    return [serialize_doc(d) for d in docs]

@router.post("/")
async def create_{name}(item: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["{name}"].insert_one(item)
    return {{"success": True, "id": str(result.inserted_id)}}

@router.put("/{{id}}")
async def update_{name}(id: str, item: dict, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["{name}"].update_one({{"_id": ObjectId(id)}}, {{"$set": item}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="{name} não encontrado")
    return {{"success": True}}

@router.delete("/{{id}}")
async def delete_{name}(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    result = await db["{name}"].delete_one({{"_id": ObjectId(id)}})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="{name} não encontrado")
    return {{"success": True}}
"""

async def ensure_data(collections):
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    for col in collections:
        count = await db[col].count_documents({})
        if count == 0:
            await db[col].insert_one(TEST_DOC)
            print(f"⚡ Inserido documento de teste em '{col}'")
        else:
            print(f"📂 Coleção '{col}' já tem {count} documentos")

def main():
    os.makedirs(ROUTERS_DIR, exist_ok=True)

    # Coleções que você listou no consultslt_db
    collections = [
        "alertas","auditorias","certidoes","certidoes_empresa","configuracoes",
        "dashboard_metrics","dashboard_snapshots","debitos","documentos",
        "documentos_empresa","empresas","fiscal","fiscal_data","fiscal_iris",
        "guias","health_check","obrigacoes","obrigacoes_empresa","ocr_documentos",
        "relatorios","relatorios_gerados","robots","robots_status","sharepoint_status",
        "status_checks","tenants","tipos_certidoes","tipos_documentos",
        "tipos_obrigacoes","tipos_relatorios","usuarios"
    ]

    # Gera routers CRUD
    for col in collections:
        path = os.path.join(ROUTERS_DIR, f"{col}.py")
        with open(path, "w", encoding="utf-8") as f:
            f.write(TEMPLATE.format(name=col))
        print(f"✔ Router atualizado: {path}")

    # Insere dados de teste em coleções vazias
    asyncio.run(ensure_data(collections))

if __name__ == "__main__":
    main()

"""
Cria automaticamente as collections ausentes no MongoDB
com base nas rotas detectadas
"""

from pymongo import MongoClient

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt"

collections_required = [
    "alertas",
    "auditoria",
    "auth",
    "dashboard",
    "empresas",
    "fiscal"
]

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

existing = db.list_collection_names()

print("🛠️ Criando collections faltantes...\n")

for col in collections_required:
    if col not in existing:
        db.create_collection(col)
        print(f"✅ Collection criada: {col}")
    else:
        print(f"✔️ Collection já existe: {col}")

print("\n🎯 MongoDB alinhado com a API.")
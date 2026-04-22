"""
Valida se as rotas reais da API possuem collections MongoDB correspondentes
"""

import sys
import os

# Garante que a raiz do projeto esteja no PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.main_enterprise import app
from pymongo import MongoClient

# ===============================
# Configuração MongoDB
# ===============================
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt"

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

# ===============================
# Rotas a ignorar
# ===============================
IGNORE_PREFIXES = (
    "/docs",
    "/redoc",
    "/openapi.json",
    "/health"
)

print("🔍 Verificando rotas x collections...\n")

collections = db.list_collection_names()
missing = set()

for route in app.routes:
    if not hasattr(route, "path"):
        continue

    path = route.path

    # Ignora rotas internas
    if path.startswith(IGNORE_PREFIXES):
        continue

    # Considera apenas rotas da API
    if not path.startswith("/api/"):
        continue

    # Ex: /api/empresas/{id} → empresas
    parts = path.replace("/api/", "").split("/")
    resource = parts[0]

    if resource and resource not in collections:
        missing.add(resource)

if not missing:
    print("✅ Todas as collections necessárias existem.")
else:
    print("❌ Collections ausentes:")
    for m in sorted(missing):
        print(f" - {m}")

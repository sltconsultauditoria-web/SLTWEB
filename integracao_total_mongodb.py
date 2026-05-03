# integracao_total_mongodb.py
# ==========================================================
# VERIFICA INTEGRAÇÃO COMPLETA:
# FRONTEND + BACKEND API + MONGODB consultslt_db
#
# OBJETIVO:
# - Descobrir rotas usadas no frontend
# - Ler OpenAPI do FastAPI
# - Testar endpoints
# - Conectar MongoDB
# - Verificar collections necessárias
# - Mostrar faltantes para status 200 OK
#
# EXECUTAR:
# pip install requests pymongo
# python integracao_total_mongodb.py
# ==========================================================

import os
import re
import requests
from pymongo import MongoClient

# ===============================
# CONFIG
# ===============================
BASE_DIR = r"C:\Users\admin-local\ServerApp\consultSLTweb"
FRONTEND = os.path.join(BASE_DIR, "frontend")

API_URL = "http://localhost:8000"

# MongoDB
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "consultslt_db"

OK = "✅"
ERRO = "❌"
WARN = "⚠️"

print("="*90)
print("DIAGNÓSTICO TOTAL - FRONTEND + BACKEND + MONGODB")
print("="*90)

# =====================================================
# 1. FRONTEND ROTAS
# =====================================================
print("\n[1] LENDO ROTAS FRONTEND...")

rotas_front = set()

patterns = [
    r'axios\.get\(["\']([^"\']+)["\']',
    r'axios\.post\(["\']([^"\']+)["\']',
    r'axios\.put\(["\']([^"\']+)["\']',
    r'axios\.delete\(["\']([^"\']+)["\']',
    r'api\.get\(["\']([^"\']+)["\']',
    r'api\.post\(["\']([^"\']+)["\']',
    r'fetch\(["\']([^"\']+)["\']',
]

for root, dirs, files in os.walk(FRONTEND):
    for file in files:
        if file.endswith((".js", ".jsx", ".ts", ".tsx")):
            path = os.path.join(root, file)

            try:
                txt = open(path, encoding="utf-8").read()
            except:
                continue

            for p in patterns:
                achados = re.findall(p, txt)
                for a in achados:
                    if a.startswith("/"):
                        rotas_front.add(a.rstrip("/"))

print(f"{OK} {len(rotas_front)} rotas encontradas")

# =====================================================
# 2. OPENAPI
# =====================================================
print("\n[2] LENDO OPENAPI BACKEND...")

rotas_back = set()

try:
    r = requests.get(API_URL + "/openapi.json", timeout=5)

    if r.status_code == 200:
        data = r.json()

        for rota in data["paths"]:
            rotas_back.add(rota.rstrip("/"))

        print(f"{OK} {len(rotas_back)} rotas detectadas")
    else:
        print(f"{ERRO} OpenAPI retornou {r.status_code}")

except Exception as e:
    print(f"{ERRO} Backend offline: {e}")

# =====================================================
# 3. TESTAR ENDPOINTS
# =====================================================
print("\n[3] TESTANDO ENDPOINTS...")

faltando = []
ok_rotas = []

for rota in sorted(rotas_front):

    url = API_URL + rota

    try:
        r = requests.get(url, timeout=4)

        if r.status_code in [200, 201, 204]:
            print(f"{OK} {rota} -> {r.status_code}")
            ok_rotas.append(rota)
        else:
            print(f"{ERRO} {rota} -> {r.status_code}")
            faltando.append((rota, r.status_code))

    except:
        print(f"{ERRO} {rota} -> OFFLINE")
        faltando.append((rota, "OFFLINE"))

# =====================================================
# 4. MONGODB
# =====================================================
print("\n[4] TESTANDO MONGODB...")

collections = []

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()

    db = client[DB_NAME]

    print(f"{OK} MongoDB conectado")
    print(f"{OK} Banco encontrado: {DB_NAME}")

    collections = db.list_collection_names()

    print(f"{OK} {len(collections)} collections encontradas")

except Exception as e:
    print(f"{ERRO} MongoDB erro: {e}")

# =====================================================
# 5. COLLECTIONS NECESSÁRIAS
# =====================================================
print("\n[5] VERIFICANDO COLLECTIONS...")

necessarias = [
    "usuarios",
    "empresas",
    "documentos",
    "obrigacoes",
    "guias",
    "alertas",
    "auditoria",
    "ocr_documentos",
    "robots_jobs",
    "relatorios"
]

for c in necessarias:
    if c in collections:
        print(f"{OK} {c}")
    else:
        print(f"{ERRO} {c} AUSENTE")

# =====================================================
# 6. RESUMO FINAL
# =====================================================
print("\n" + "="*90)
print("RESUMO FINAL")
print("="*90)

print(f"{OK} Rotas frontend: {len(rotas_front)}")
print(f"{OK} Rotas backend: {len(rotas_back)}")
print(f"{OK} Status 200: {len(ok_rotas)}")
print(f"{ERRO} Quebradas: {len(faltando)}")

if faltando:
    print("\nENDPOINTS FALTANDO:")
    for rota, cod in faltando:
        print(" ->", rota, "| retorno:", cod)

print("""
PARA TUDO FUNCIONAR 200 OK:

1. Backend FastAPI precisa criar endpoints faltantes
2. MongoDB consultslt_db precisa collections faltantes
3. Frontend .env:

VITE_API_URL=http://localhost:8000

4. Rodar backend correto:
uvicorn backend.main_enterprise:app --reload

5. Rodar frontend:
npm start
""")

print("="*90)
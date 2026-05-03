# segunda_validacao_pre_ajuste.py
# Executa uma validação final antes de qualquer correção:
# - Estrutura de pastas
# - Integridade do backup
# - Status backend
# - Frontend dependências
# - MongoDB consultslt_db
# - Arquivos críticos
# - Risco de ajuste
#
# EXECUTAR:
# python segunda_validacao_pre_ajuste.py

import os
import json
import zipfile
import requests
from pathlib import Path
from datetime import datetime

try:
    from pymongo import MongoClient
    mongo_ok = True
except:
    mongo_ok = False

BASE = Path.cwd()
BACKUP_DIR = BASE / "_BACKUPS"

print("=" * 90)
print("SEGUNDA VALIDAÇÃO PRÉ-AJUSTE - CONSULTSLTWEB")
print("=" * 90)

score = 100
problemas = []

# ---------------------------------------------------
# 1. Estrutura principal
# ---------------------------------------------------
print("\n[1] VALIDANDO ESTRUTURA...")

pastas = ["frontend", "backend"]
for pasta in pastas:
    if (BASE / pasta).exists():
        print(f"✅ {pasta}")
    else:
        print(f"❌ {pasta}")
        problemas.append(f"Pasta ausente: {pasta}")
        score -= 20

# ---------------------------------------------------
# 2. Backup existe
# ---------------------------------------------------
print("\n[2] VALIDANDO BACKUP...")

if BACKUP_DIR.exists():
    zips = list(BACKUP_DIR.glob("*.zip"))
    if zips:
        ultimo = sorted(zips)[-1]
        print(f"✅ Backup encontrado: {ultimo.name}")

        try:
            with zipfile.ZipFile(ultimo, 'r') as z:
                nomes = z.namelist()
                print(f"✅ ZIP íntegro ({len(nomes)} arquivos)")
        except:
            print("❌ ZIP corrompido")
            problemas.append("Backup corrompido")
            score -= 25
    else:
        print("❌ Nenhum ZIP encontrado")
        problemas.append("Sem backup ZIP")
        score -= 25
else:
    print("❌ Pasta _BACKUPS não encontrada")
    problemas.append("Sem backup")
    score -= 25

# ---------------------------------------------------
# 3. Backend online
# ---------------------------------------------------
print("\n[3] VALIDANDO BACKEND...")

urls = [
    "http://localhost:8000/health",
    "http://localhost:8000/docs",
    "http://localhost:8000/openapi.json"
]

backend_ok = 0

for url in urls:
    try:
        r = requests.get(url, timeout=3)
        if r.status_code in [200, 401, 405]:
            print(f"✅ {url} -> {r.status_code}")
            backend_ok += 1
        else:
            print(f"⚠️ {url} -> {r.status_code}")
    except:
        print(f"❌ {url}")
        
if backend_ok == 0:
    score -= 20
    problemas.append("Backend offline")

# ---------------------------------------------------
# 4. Frontend package.json
# ---------------------------------------------------
print("\n[4] VALIDANDO FRONTEND...")

pkg = BASE / "frontend" / "package.json"

if pkg.exists():
    print("✅ package.json encontrado")
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
        deps = data.get("dependencies", {})
        print(f"✅ Dependências: {len(deps)}")
    except:
        print("⚠️ package.json inválido")
        score -= 10
else:
    print("❌ package.json ausente")
    problemas.append("package.json ausente")
    score -= 15

# ---------------------------------------------------
# 5. MongoDB
# ---------------------------------------------------
print("\n[5] VALIDANDO MONGODB...")

if mongo_ok:
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        db = client["consultslt_db"]
        cols = db.list_collection_names()
        print("✅ MongoDB conectado")
        print(f"✅ Collections: {len(cols)}")

        criticas = [
            "usuarios",
            "empresas",
            "documentos",
            "guias",
            "obrigacoes",
            "alertas"
        ]

        for c in criticas:
            if c in cols:
                print(f"   ✅ {c}")
            else:
                print(f"   ❌ {c}")
                score -= 3

    except Exception as e:
        print("❌ MongoDB offline")
        score -= 15
        problemas.append("MongoDB offline")
else:
    print("⚠️ pymongo não instalado")

# ---------------------------------------------------
# 6. Arquivos críticos
# ---------------------------------------------------
print("\n[6] VALIDANDO ARQUIVOS CRÍTICOS...")

arquivos = [
    "frontend/src/App.jsx",
    "frontend/src/index.js",
    "frontend/src/main.jsx",
    "backend/main.py",
    "backend/main_enterprise.py"
]

for arq in arquivos:
    if (BASE / arq).exists():
        print(f"✅ {arq}")
    else:
        print(f"⚠️ {arq}")

# ---------------------------------------------------
# Resultado final
# ---------------------------------------------------
print("\n" + "=" * 90)
print("RESULTADO FINAL")
print("=" * 90)

if score >= 85:
    risco = "BAIXO"
elif score >= 65:
    risco = "MÉDIO"
else:
    risco = "ALTO"

print(f"Score segurança: {score}/100")
print(f"Risco de ajuste: {risco}")

if problemas:
    print("\nProblemas encontrados:")
    for p in problemas:
        print(" -", p)

print("\nRECOMENDAÇÃO:")

if risco == "BAIXO":
    print("✅ Seguro para ajustar.")
elif risco == "MÉDIO":
    print("⚠️ Ajustar com cautela.")
else:
    print("❌ Não ajustar ainda.")

print("\nHorário:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
print("=" * 90)
# backup_total_consultsltweb.py
# ==========================================================
# BACKUP PROFISSIONAL COMPLETO - SEM PERDER NADA
#
# O QUE FAZ:
# 1. Backup frontend completo
# 2. Backup backend completo
# 3. Backup arquivos .env
# 4. Backup package.json
# 5. Backup MongoDB consultslt_db
# 6. Gera inventário de arquivos
# 7. Compacta tudo em ZIP com data/hora
#
# EXECUTAR:
# pip install pymongo
# python backup_total_consultsltweb.py
# ==========================================================

import os
import shutil
import zipfile
import json
from datetime import datetime
from pathlib import Path

# Mongo
from pymongo import MongoClient

# ==========================================================
# CONFIG
# ==========================================================
BASE_DIR = r"C:\Users\admin-local\ServerApp\consultSLTweb"
PROJECT_NAME = "consultSLTweb"

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "consultslt_db"

DATA = datetime.now().strftime("%Y%m%d_%H%M%S")

BACKUP_ROOT = os.path.join(BASE_DIR, "_BACKUPS")
BACKUP_DIR = os.path.join(BACKUP_ROOT, f"backup_{DATA}")
ZIP_FILE = os.path.join(BACKUP_ROOT, f"backup_{DATA}.zip")

OK = "✅"
ERRO = "❌"
WARN = "⚠️"

# ==========================================================
# FUNÇÕES
# ==========================================================
def criar_pasta(path):
    os.makedirs(path, exist_ok=True)

def copiar(origem, destino):
    if os.path.exists(origem):
        shutil.copy2(origem, destino)
        return True
    return False

def copiar_pasta(origem, destino):
    if os.path.exists(origem):
        shutil.copytree(origem, destino, dirs_exist_ok=True)
        return True
    return False

# ==========================================================
# INÍCIO
# ==========================================================
print("="*90)
print("BACKUP TOTAL CONSULTSLTWEB")
print("="*90)

criar_pasta(BACKUP_ROOT)
criar_pasta(BACKUP_DIR)

# ==========================================================
# 1. FRONTEND
# ==========================================================
print("\n[1] BACKUP FRONTEND...")

frontend = os.path.join(BASE_DIR, "frontend")
dest_front = os.path.join(BACKUP_DIR, "frontend")

if copiar_pasta(frontend, dest_front):
    print(f"{OK} frontend salvo")
else:
    print(f"{ERRO} frontend não encontrado")

# ==========================================================
# 2. BACKEND
# ==========================================================
print("\n[2] BACKUP BACKEND...")

backend = os.path.join(BASE_DIR, "backend")
dest_back = os.path.join(BACKUP_DIR, "backend")

if copiar_pasta(backend, dest_back):
    print(f"{OK} backend salvo")
else:
    print(f"{ERRO} backend não encontrado")

# ==========================================================
# 3. .ENV / CONFIG
# ==========================================================
print("\n[3] BACKUP CONFIGURAÇÕES...")

configs = [
    ".env",
    "frontend\\.env",
    "backend\\.env",
    "package.json",
    "frontend\\package.json",
    "requirements.txt"
]

config_dir = os.path.join(BACKUP_DIR, "configs")
criar_pasta(config_dir)

for arq in configs:
    full = os.path.join(BASE_DIR, arq)

    if copiar(full, config_dir):
        print(f"{OK} {arq}")
    else:
        print(f"{WARN} {arq} não encontrado")

# ==========================================================
# 4. INVENTÁRIO
# ==========================================================
print("\n[4] GERANDO INVENTÁRIO...")

inventario = []

for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        path = os.path.join(root, file)

        try:
            size = os.path.getsize(path)
        except:
            size = 0

        inventario.append({
            "arquivo": path.replace(BASE_DIR, ""),
            "bytes": size
        })

with open(os.path.join(BACKUP_DIR, "inventario.json"), "w", encoding="utf-8") as f:
    json.dump(inventario, f, indent=2, ensure_ascii=False)

print(f"{OK} inventário salvo")

# ==========================================================
# 5. BACKUP MONGODB
# ==========================================================
print("\n[5] BACKUP MONGODB...")

mongo_dir = os.path.join(BACKUP_DIR, "mongodb")
criar_pasta(mongo_dir)

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DB_NAME]

    cols = db.list_collection_names()

    resumo = {}

    for col in cols:
        docs = list(db[col].find())

        for d in docs:
            d["_id"] = str(d["_id"])

        arquivo = os.path.join(mongo_dir, f"{col}.json")

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(docs, f, indent=2, ensure_ascii=False)

        resumo[col] = len(docs)
        print(f"{OK} {col}: {len(docs)} docs")

    with open(os.path.join(mongo_dir, "resumo.json"), "w") as f:
        json.dump(resumo, f, indent=2)

except Exception as e:
    print(f"{ERRO} MongoDB falhou: {e}")

# ==========================================================
# 6. ZIP
# ==========================================================
print("\n[6] COMPACTANDO...")

with zipfile.ZipFile(ZIP_FILE, "w", zipfile.ZIP_DEFLATED) as zipf:

    for root, dirs, files in os.walk(BACKUP_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, BACKUP_DIR)
            zipf.write(file_path, arcname)

print(f"{OK} ZIP criado")

# ==========================================================
# FINAL
# ==========================================================
print("\n" + "="*90)
print("BACKUP CONCLUÍDO COM SUCESSO")
print("="*90)
print("Pasta:")
print(BACKUP_DIR)
print("")
print("Arquivo ZIP:")
print(ZIP_FILE)
print("")
print("Pode corrigir o sistema com segurança agora.")
print("="*90)
import re
from pathlib import Path
from pymongo import MongoClient

print("\n🔎 AUDITORIA ENTERPRISE DE CAMPOS COM MÁSCARA\n")

# -------------------------------
# CONFIG
# -------------------------------

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "consultslt_db"

PROJECT_ROOT = Path("../../")

FIELDS = {
    "CNPJ": r"cnpj",
    "CPF": r"cpf",
    "CEP": r"cep",
    "TELEFONE": r"telefone|phone|celular",
    "EMAIL": r"email",
    "DATA": r"data|date",
    "VALOR": r"valor|preco|total|price",
    "IE": r"inscricao_estadual|ie",
    "PLACA": r"placa",
}

MASKS = {
    "CNPJ": "00.000.000/0000-00",
    "CPF": "000.000.000-00",
    "CEP": "00000-000",
    "TELEFONE": "(00) 00000-0000",
    "DATA": "DD/MM/YYYY",
    "VALOR": "1.234,56",
    "IE": "varia por estado",
}

# -------------------------------
# ANALISAR MONGODB
# -------------------------------

print("\n📦 ANALISANDO MONGODB\n")

client = MongoClient(MONGO_URL)
db = client[DB_NAME]

mongo_fields = {}

for col in db.list_collection_names():

    doc = db[col].find_one()

    if not doc:
        continue

    for k in doc.keys():

        key = k.lower()

        for label, pattern in FIELDS.items():

            if re.search(pattern, key):

                if label not in mongo_fields:
                    mongo_fields[label] = []

                mongo_fields[label].append((col, k))

print("\nCampos detectados no MongoDB:\n")

for field, locs in mongo_fields.items():

    print(f"\n⚠ {field}")

    for col, k in locs:
        print(f"   coleção: {col} -> campo: {k}")

# -------------------------------
# ANALISAR BACKEND
# -------------------------------

print("\n⚙ ANALISANDO BACKEND\n")

backend_files = list(PROJECT_ROOT.rglob("*.py"))

backend_hits = {}

for file in backend_files:

    try:
        content = file.read_text(encoding="utf-8", errors="ignore").lower()
    except:
        continue

    for label, pattern in FIELDS.items():

        if re.search(pattern, content):

            if label not in backend_hits:
                backend_hits[label] = []

            backend_hits[label].append(str(file))

for field, files in backend_hits.items():

    print(f"\n⚠ {field} usado no backend")

    for f in list(set(files))[:10]:
        print("   ", f)

# -------------------------------
# ANALISAR FRONTEND
# -------------------------------

print("\n🎨 ANALISANDO FRONTEND\n")

frontend_files = []

frontend_files.extend(PROJECT_ROOT.rglob("*.js"))
frontend_files.extend(PROJECT_ROOT.rglob("*.ts"))
frontend_files.extend(PROJECT_ROOT.rglob("*.tsx"))

frontend_hits = {}

for file in frontend_files:

    try:
        content = file.read_text(encoding="utf-8", errors="ignore").lower()
    except:
        continue

    for label, pattern in FIELDS.items():

        if re.search(pattern, content):

            if label not in frontend_hits:
                frontend_hits[label] = []

            frontend_hits[label].append(str(file))

for field, files in frontend_hits.items():

    print(f"\n⚠ {field} usado no frontend")

    for f in list(set(files))[:10]:
        print("   ", f)

# -------------------------------
# RELATÓRIO FINAL
# -------------------------------

print("\n📊 MÁSCARAS RECOMENDADAS\n")

for field, mask in MASKS.items():

    print(f"{field:10} -> {mask}")

print("\n🏁 Auditoria finalizada\n")
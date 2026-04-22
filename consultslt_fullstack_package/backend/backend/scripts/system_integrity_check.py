import os
import re
from pymongo import MongoClient

print("\n🚀 CONSULT SLT - SYSTEM INTEGRITY CHECK\n")

ROOT = "../../"

IGNORE = [
    "node_modules",
    "venv",
    "__pycache__",
    ".git",
    "build",
    "dist"
]

MOCK_WORDS = [
    "mock",
    "fake",
    "dummy",
    "sample",
    "hardcoded",
]

STATIC_PATTERNS = [
    r"=\s*\[",
    r"=\s*\{"
]

# ---------------------------------------------------
# MongoDB
# ---------------------------------------------------

print("\n📦 CONECTANDO AO MONGODB\n")

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

collections = sorted(db.list_collection_names())

print("Coleções encontradas:")

for c in collections:
    print(" ", c)

# ---------------------------------------------------
# Backend routers
# ---------------------------------------------------

print("\n⚙ ANALISANDO BACKEND ROUTERS\n")

routers = set()

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    if "router" in root or "routers" in root:

        for file in files:

            if file.endswith(".py"):

                name = file.replace(".py","")

                if name not in ["__init__"]:
                    routers.add(name)

routers = sorted(list(routers))

print("Routers encontrados:")

for r in routers:
    print(" ", r)

# ---------------------------------------------------
# Collection x Router
# ---------------------------------------------------

print("\n🔎 COLLECTION ↔ ROUTER\n")

for col in collections:

    if col not in routers:
        print("⚠ coleção sem router:", col)

for r in routers:

    if r not in collections and r not in ["auth","dashboard","ecac","sharepoint"]:
        print("⚠ router sem coleção:", r)

# ---------------------------------------------------
# Frontend endpoints
# ---------------------------------------------------

print("\n🎨 ANALISANDO FRONTEND\n")

api_calls = set()

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith((".js",".jsx",".ts",".tsx")):

            path = os.path.join(root,file)

            try:

                with open(path,"r",encoding="utf8") as f:

                    content = f.read()

                    matches = re.findall(r"/api/([a-zA-Z0-9_-]+)",content)

                    for m in matches:
                        api_calls.add(m)

            except:
                pass

api_calls = sorted(list(api_calls))

print("Endpoints usados no frontend:")

for c in api_calls:
    print(" ", c)

# ---------------------------------------------------
# Frontend x Backend
# ---------------------------------------------------

print("\n🔎 FRONTEND ↔ BACKEND\n")

for call in api_calls:

    if call not in routers:
        print("⚠ endpoint usado no frontend sem router:", call)

# ---------------------------------------------------
# Detectar mocks
# ---------------------------------------------------

print("\n🧪 PROCURANDO MOCK DATA\n")

mock_files = set()

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith((".py",".js",".jsx",".ts",".tsx")):

            path = os.path.join(root,file)

            try:

                with open(path,"r",encoding="utf8") as f:

                    content = f.read().lower()

                    for w in MOCK_WORDS:

                        if w in content:
                            mock_files.add(path)

            except:
                pass

if mock_files:

    print("\n⚠ possíveis mocks encontrados:\n")

    for f in sorted(list(mock_files))[:20]:
        print(" ",f)

else:
    print("✅ nenhum mock encontrado")

# ---------------------------------------------------
# Detectar dados estáticos
# ---------------------------------------------------

print("\n📊 PROCURANDO DADOS ESTÁTICOS\n")

static_files = set()

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith((".js",".jsx",".ts",".tsx")):

            path = os.path.join(root,file)

            try:

                with open(path,"r",encoding="utf8") as f:

                    content = f.read()

                    for p in STATIC_PATTERNS:

                        if re.search(p,content):
                            static_files.add(path)

            except:
                pass

if static_files:

    print("\n⚠ possíveis dados estáticos:\n")

    for f in sorted(list(static_files))[:20]:
        print(" ",f)

else:

    print("✅ nenhum dado estático encontrado")

# ---------------------------------------------------
# Verificar duplicidade usuarios/users
# ---------------------------------------------------

print("\n👥 VERIFICANDO USERS / USUARIOS\n")

if "users" in routers and "usuarios" in routers:

    print("⚠ duplicidade detectada: users / usuarios")
    print("👉 recomendado manter apenas: usuarios")

# ---------------------------------------------------
# Verificar índices importantes
# ---------------------------------------------------

print("\n📈 VERIFICANDO ÍNDICES CRÍTICOS\n")

important = [
    "cnpj",
    "empresa_id",
    "created_at",
    "updated_at",
    "status"
]

for col in collections:

    collection = db[col]

    indexes = collection.index_information()

    index_fields = []

    for idx in indexes.values():

        if "key" in idx:

            for k in idx["key"]:
                index_fields.append(k[0])

    for field in important:

        if field not in index_fields:

            print(f"⚠ {col} sem índice:", field)

# ---------------------------------------------------

print("\n🏁 VERIFICAÇÃO FINALIZADA\n")
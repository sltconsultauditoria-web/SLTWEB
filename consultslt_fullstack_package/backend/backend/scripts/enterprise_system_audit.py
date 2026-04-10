import os
import re
from pymongo import MongoClient

print("\n🚀 ENTERPRISE SYSTEM AUDIT\n")

ROOT = "../../"

IGNORE = [
    "node_modules",
    "venv",
    "__pycache__",
    ".git",
    "archive"
]

MOCK_WORDS = [
    "mock",
    "fake",
    "dummy",
    "sample",
    "static",
    "hardcoded"
]

# -----------------------------
# MongoDB
# -----------------------------

print("\n📦 LENDO MONGODB\n")

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

collections = db.list_collection_names()

print("Coleções encontradas:")

for c in collections:
    print("  ", c)

# -----------------------------
# Backend routers
# -----------------------------

print("\n⚙ ANALISANDO BACKEND ROUTERS\n")

routers = []

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith(".py") and "router" in root:

            name = file.replace(".py", "")
            routers.append(name)

print("Routers encontrados:")

for r in routers:
    print(" ", r)

# -----------------------------
# Verificar router x collection
# -----------------------------

print("\n🔎 VERIFICANDO COLLECTION ↔ ROUTER\n")

for col in collections:

    if col not in routers:
        print(f"⚠ coleção sem router: {col}")

for r in routers:

    if r not in collections:
        print(f"⚠ router sem coleção: {r}")

# -----------------------------
# Frontend API calls
# -----------------------------

print("\n🎨 ANALISANDO FRONTEND\n")

api_calls = []

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith((".js", ".ts", ".jsx", ".tsx")):

            path = os.path.join(root, file)

            try:

                with open(path, "r", encoding="utf8") as f:

                    content = f.read()

                    matches = re.findall(r"/api/([a-zA-Z0-9_-]+)", content)

                    for m in matches:
                        api_calls.append(m)

            except:
                pass

api_calls = list(set(api_calls))

print("\nEndpoints usados no frontend:")

for c in api_calls:
    print(" ", c)

# -----------------------------
# Verificar frontend x backend
# -----------------------------

print("\n🔎 FRONTEND ↔ BACKEND\n")

for call in api_calls:

    if call not in routers:
        print(f"⚠ endpoint frontend sem router: {call}")

# -----------------------------
# Mock data detector
# -----------------------------

print("\n🧪 DETECTANDO MOCK DATA\n")

mock_files = []

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith((".py",".js",".ts",".jsx",".tsx")):

            path = os.path.join(root, file)

            try:

                with open(path, "r", encoding="utf8") as f:

                    content = f.read().lower()

                    for word in MOCK_WORDS:

                        if word in content:
                            mock_files.append(path)

            except:
                pass

mock_files = list(set(mock_files))

if mock_files:

    print("\n⚠ arquivos com possíveis mocks:\n")

    for f in mock_files[:20]:
        print(" ", f)

else:

    print("\n✅ nenhum mock detectado")

# -----------------------------
# Static arrays detector
# -----------------------------

print("\n📊 DETECTANDO DADOS ESTÁTICOS\n")

static_patterns = [
    r"=\s*\[",
    r"=\s*\{"
]

static_files = []

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith((".js",".ts",".jsx",".tsx")):

            path = os.path.join(root, file)

            try:

                with open(path,"r",encoding="utf8") as f:

                    content = f.read()

                    for p in static_patterns:

                        if re.search(p, content):
                            static_files.append(path)

            except:
                pass

static_files = list(set(static_files))

print("\n⚠ arquivos com possíveis dados estáticos:\n")

for f in static_files[:20]:
    print(" ",f)

print("\n🏁 AUDITORIA FINALIZADA\n")
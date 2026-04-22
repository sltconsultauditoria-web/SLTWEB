import os
import re
from pymongo import MongoClient

print("\n🚀 CONSULT SLT - ENTERPRISE SYSTEM INSPECTOR\n")

ROOT = "../../"

IGNORE = [
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "build",
    "dist",
    "backup"
]

# -----------------------------
# MongoDB
# -----------------------------

print("📦 LENDO MONGODB\n")

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

collections = db.list_collection_names()

print("Coleções encontradas:", len(collections))

for c in collections:
    print(" ", c)

# -----------------------------
# Routers
# -----------------------------

print("\n⚙ LENDO ROUTERS\n")

routers = []

for root, dirs, files in os.walk(ROOT):

    if any(i in root for i in IGNORE):
        continue

    if "router" in root or "api" in root:

        for f in files:

            if f.endswith(".py") and f != "__init__.py":

                routers.append(f.replace(".py",""))

routers = sorted(list(set(routers)))

print("Routers encontrados:", len(routers))

for r in routers:
    print(" ", r)

# -----------------------------
# Frontend endpoints
# -----------------------------

print("\n🎨 ANALISANDO FRONTEND\n")

frontend_calls = set()

for root, dirs, files in os.walk(ROOT):

    if any(i in root for i in IGNORE):
        continue

    for f in files:

        if f.endswith((".js",".jsx",".ts",".tsx")):

            path = os.path.join(root,f)

            try:

                with open(path,"r",encoding="utf8") as file:

                    content = file.read()

                    matches = re.findall(r"/api/([a-zA-Z0-9_-]+)",content)

                    for m in matches:
                        frontend_calls.add(m)

            except:
                pass

print("Endpoints usados no frontend:", len(frontend_calls))

for e in sorted(frontend_calls):
    print(" ", e)

# -----------------------------
# Persistência Mongo
# -----------------------------

print("\n💾 VERIFICANDO PERSISTÊNCIA MONGODB\n")

mongo_patterns = [
    "insert_one",
    "find(",
    "update_one",
    "delete_one"
]

persistent_modules = []

for root, dirs, files in os.walk(ROOT):

    if any(i in root for i in IGNORE):
        continue

    for f in files:

        if f.endswith(".py"):

            path = os.path.join(root,f)

            try:

                with open(path,"r",encoding="utf8") as file:

                    content = file.read()

                    if any(p in content for p in mongo_patterns):

                        persistent_modules.append(f.replace(".py",""))

            except:
                pass

persistent_modules = sorted(list(set(persistent_modules)))

print("Módulos com persistência Mongo:", len(persistent_modules))

for p in persistent_modules:
    print(" ", p)

# -----------------------------
# Mapear sistema
# -----------------------------

print("\n🧠 MAPA DO SISTEMA\n")

for module in routers:

    status = []

    if module in collections:
        status.append("Mongo")

    if module in frontend_calls:
        status.append("Frontend")

    if module in persistent_modules:
        status.append("Persistência")

    if status:
        print(f"✅ {module} → {', '.join(status)}")
    else:
        print(f"⚠ {module} → possivelmente órfão")

print("\n🏁 INSPEÇÃO FINALIZADA\n")
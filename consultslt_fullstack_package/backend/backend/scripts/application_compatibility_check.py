import os
import re
from pymongo import MongoClient

print("\n🚀 CONSULT SLT - APPLICATION COMPATIBILITY CHECK\n")

ROOT = "../../"

IGNORE = [
    "node_modules",
    "venv",
    "__pycache__",
    ".git",
    "build",
    "dist"
]

# ---------------------------------------------------
# MongoDB
# ---------------------------------------------------

print("\n📦 LENDO MONGODB\n")

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

collections = db.list_collection_names()

print("Coleções:")

for c in collections:
    print(" ", c)

# ---------------------------------------------------
# Routers
# ---------------------------------------------------

print("\n⚙ LENDO ROUTERS\n")

routers = []

for root, dirs, files in os.walk(ROOT):

    if "routers" in root:

        for file in files:

            if file.endswith(".py"):

                name = file.replace(".py","")

                if name != "__init__":
                    routers.append(name)

print("Routers:")

for r in routers:
    print(" ", r)

# ---------------------------------------------------
# Frontend endpoints
# ---------------------------------------------------

print("\n🎨 ANALISANDO FRONTEND\n")

frontend_calls = set()

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
                        frontend_calls.add(m)

            except:
                pass

print("Endpoints usados no frontend:")

for e in frontend_calls:
    print(" ",e)

# ---------------------------------------------------
# Verificar compatibilidade
# ---------------------------------------------------

print("\n🔎 VERIFICAÇÃO DE COMPATIBILIDADE\n")

valid_modules = []

for col in collections:

    if col in routers:

        if col in frontend_calls:

            print(f"✅ módulo completo: {col}")

            valid_modules.append(col)

        else:

            print(f"⚠ usado no backend mas não no frontend: {col}")

    else:

        print(f"⚠ coleção sem router: {col}")

# ---------------------------------------------------
# Routers sem frontend
# ---------------------------------------------------

print("\n⚙ ROUTERS SEM USO NO FRONTEND\n")

for r in routers:

    if r not in frontend_calls and r not in ["auth","dashboard"]:

        print("⚠ possível router não utilizado:", r)

# ---------------------------------------------------
# Arquivos órfãos
# ---------------------------------------------------

print("\n📁 PROCURANDO ARQUIVOS ÓRFÃOS\n")

used_words = valid_modules + routers

orphans = []

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith(".py"):

            path = os.path.join(root,file)

            try:

                with open(path,"r",encoding="utf8") as f:

                    content = f.read()

                    found = False

                    for word in used_words:

                        if word in content:

                            found = True
                            break

                    if not found:

                        orphans.append(path)

            except:
                pass

print("\n⚠ POSSÍVEIS ARQUIVOS NÃO UTILIZADOS\n")

for o in orphans[:30]:
    print(" ",o)

print("\n🏁 AUDITORIA FINALIZADA\n")
import os
import re

print("\n🚀 CONSULT SLT - REAL CRUD DETECTOR\n")

ROOT = "../../backend"

IGNORE = [
    "venv",
    "__pycache__",
    "node_modules",
    ".git",
    "scripts",
    "backup",
    "build",
    "dist"
]

routers = []

# -----------------------------
# Encontrar routers reais
# -----------------------------

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    if "routers" in root or "api" in root:

        for file in files:

            if file.endswith(".py") and file != "__init__.py":

                routers.append(os.path.join(root,file))

routers = list(set(routers))

print("Routers reais encontrados:",len(routers),"\n")

# -----------------------------
# CRUD patterns
# -----------------------------

crud_patterns = {
    "create": ["insert_one","insert_many"],
    "read": ["find(","find_one"],
    "update": ["update_one","update_many"],
    "delete": ["delete_one","delete_many"]
}

mock_patterns = [
    "fake_data",
    "example_data",
    "mock_data",
    "data = [",
    "return [ {",
]

# -----------------------------
# Auditoria
# -----------------------------

full_crud = []
partial_crud = []
mock_modules = []

for router in routers:

    try:

        with open(router,"r",encoding="utf8") as f:

            content = f.read().lower()

    except:
        continue

    crud_found = {
        "create":False,
        "read":False,
        "update":False,
        "delete":False
    }

    for crud,patterns in crud_patterns.items():

        for p in patterns:

            if p in content:
                crud_found[crud] = True

    mock_found = any(m in content for m in mock_patterns)

    module = os.path.basename(router).replace(".py","")

    if mock_found:

        mock_modules.append(module)

    elif all(crud_found.values()):

        full_crud.append(module)

    else:

        partial_crud.append(module)

# -----------------------------
# Resultado
# -----------------------------

print("✅ CRUD 100% PERSISTENTE\n")

for m in sorted(set(full_crud)):
    print(" ",m)

print("\n⚠ CRUD PARCIAL\n")

for m in sorted(set(partial_crud)):
    print(" ",m)

print("\n❌ MÓDULOS COM MOCK\n")

for m in sorted(set(mock_modules)):
    print(" ",m)

print("\n🏁 AUDITORIA FINALIZADA\n")
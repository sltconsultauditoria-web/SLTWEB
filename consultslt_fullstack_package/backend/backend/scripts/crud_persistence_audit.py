import os
import re

print("\n🚀 CONSULT SLT - CRUD PERSISTENCE AUDIT\n")

ROOT = "../../"

IGNORE = [
    "node_modules",
    "venv",
    "__pycache__",
    ".git",
    "build",
    "dist"
]

crud_patterns = {
    "create": ["insert_one","insert_many"],
    "read": ["find(","find_one"],
    "update": ["update_one","update_many"],
    "delete": ["delete_one","delete_many"]
}

mock_patterns = [
    "mock",
    "fake",
    "seed",
    "example_data",
    "test_data"
]

static_patterns = [
    "return [",
    "return {",
    "const data",
    "let data",
    "data = [",
]

routers = []

# ---------------------------------------------------
# Encontrar routers
# ---------------------------------------------------

print("🔎 Procurando routers\n")

for root, dirs, files in os.walk(ROOT):

    if "routers" in root:

        for file in files:

            if file.endswith(".py") and file != "__init__.py":

                routers.append(os.path.join(root,file))

print("Routers encontrados:",len(routers),"\n")

# ---------------------------------------------------
# Auditoria CRUD
# ---------------------------------------------------

valid_modules = []
partial_modules = []
mock_modules = []

for router in routers:

    try:

        with open(router,"r",encoding="utf8") as f:

            content = f.read().lower()

    except:
        continue

    crud_found = {
        "create": False,
        "read": False,
        "update": False,
        "delete": False
    }

    for crud, patterns in crud_patterns.items():

        for p in patterns:

            if p in content:

                crud_found[crud] = True

    mock_found = any(m in content for m in mock_patterns)
    static_found = any(s in content for s in static_patterns)

    module = os.path.basename(router).replace(".py","")

    if mock_found or static_found:

        mock_modules.append(module)

    elif all(crud_found.values()):

        valid_modules.append(module)

    else:

        partial_modules.append(module)

# ---------------------------------------------------
# Resultado
# ---------------------------------------------------

print("✅ MÓDULOS CRUD COMPLETOS (PERSISTENTES)\n")

for m in valid_modules:
    print(" ",m)

print("\n⚠ MÓDULOS CRUD PARCIAIS\n")

for m in partial_modules:
    print(" ",m)

print("\n❌ MÓDULOS COM MOCK OU DADOS ESTÁTICOS\n")

for m in mock_modules:
    print(" ",m)

# ---------------------------------------------------
# Procurar arquivos com mocks
# ---------------------------------------------------

print("\n🧪 PROCURANDO MOCKS NO PROJETO\n")

mock_files = []

for root, dirs, files in os.walk(ROOT):

    if any(x in root for x in IGNORE):
        continue

    for file in files:

        if file.endswith((".py",".js",".jsx",".ts",".tsx")):

            path = os.path.join(root,file)

            try:

                with open(path,"r",encoding="utf8") as f:

                    content = f.read().lower()

                    if any(m in content for m in mock_patterns):

                        mock_files.append(path)

            except:
                pass

for m in mock_files[:30]:
    print(" ",m)

print("\n🏁 AUDITORIA FINALIZADA\n")
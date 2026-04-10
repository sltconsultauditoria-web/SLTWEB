import os
import ast
from pathlib import Path

ROUTERS_DIR = Path("backend/routers")

print("\n🔎 AUDITORIA DE ROTAS - CONSULT SLT ENTERPRISE\n")

routers = []

for file in ROUTERS_DIR.glob("*.py"):
    if file.name == "__init__.py":
        continue

    with open(file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    router_prefix = None
    endpoints = []

    for node in ast.walk(tree):

        # Detectar APIRouter
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Call):
                if getattr(node.value.func, "id", "") == "APIRouter":
                    for kw in node.value.keywords:
                        if kw.arg == "prefix":
                            router_prefix = kw.value.value

        # Detectar endpoints
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call):
                    if hasattr(dec.func, "attr"):
                        method = dec.func.attr.upper()

                        path = "/"
                        if dec.args:
                            try:
                                path = dec.args[0].value
                            except:
                                pass

                        endpoints.append((method, path))

    routers.append({
        "file": file.stem,
        "prefix": router_prefix,
        "endpoints": endpoints
    })


# =====================================================
# ANALISE
# =====================================================

duplicates = []
suggestions = []

for r in routers:

    router_name = r["file"]
    prefix = r["prefix"]

    print(f"📦 Router: {router_name}")

    if prefix:
        print(f"⚠ Prefixo interno detectado: {prefix}")

        if prefix.strip("/") == router_name:
            suggestions.append(
                f"{router_name}.py -> REMOVER prefix='{prefix}'"
            )

    else:
        print("✅ Sem prefixo interno")

    for method, path in r["endpoints"]:

        full = f"/api/{router_name}{path}"

        if f"/{router_name}/{router_name}" in full:
            duplicates.append(full)

        print(f"   {method} {path}")

    print()


# =====================================================
# RESULTADOS
# =====================================================

print("\n==============================")
print("📊 RESULTADO DA AUDITORIA")
print("==============================\n")

if duplicates:
    print("❌ ROTAS DUPLICADAS DETECTADAS:\n")
    for d in duplicates:
        print(d)

print("\n------------------------------")

if suggestions:
    print("\n🛠 SUGESTÕES DE CORREÇÃO:\n")
    for s in suggestions:
        print("•", s)

print("\n------------------------------")

print("\n✅ PADRÃO RECOMENDADO:\n")

print("""
router = APIRouter()

@router.get("/")
def listar():
    ...
""")

print("""
main_enterprise.py:

prefix = f"/api/{router_file.stem}"
app.include_router(module.router, prefix=prefix)
""")

print("\n🏁 Auditoria concluída\n")
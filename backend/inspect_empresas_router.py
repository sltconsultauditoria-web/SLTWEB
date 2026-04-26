from backend.utils.mongo_serializer import serialize_mongo
import ast
from pathlib import Path

FILE = Path("routers/empresas.py")

print("🔍 Analisando empresas.py...\n")

with open(FILE, "r", encoding="utf-8") as f:
    tree = ast.parse(f.read())

prefix = None
routes = []

for node in ast.walk(tree):

    # Detectar prefix
    if isinstance(node, ast.Call):
        if hasattr(node.func, "id") and node.func.id == "APIRouter":
            for kw in node.keywords:
                if kw.arg == "prefix" and isinstance(kw.value, ast.Constant):
                    prefix = kw.value.value

    # Detectar endpoints
    if isinstance(node, ast.FunctionDef):
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Call) and hasattr(decorator.func, "attr"):
                method = decorator.func.attr.upper()
                if method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    if decorator.args and isinstance(decorator.args[0], ast.Constant):
                        path = decorator.args[0].value
                        routes.append((method, path))

print(f"📦 Prefixo encontrado: {prefix}\n")

print("🛣 Rotas encontradas:\n")
for method, path in routes:
    full = f"{prefix}{path}" if prefix else path
    print(f"{method} -> {path}   | Final: {full}")

print("\n🚨 Verificando duplicação de segmento...\n")

if prefix:
    base_segment = prefix.strip("/").split("/")[-1]

    for method, path in routes:
        if base_segment in path:
            print(f"⚠ POSSÍVEL DUPLICAÇÃO: {method} {path}")

print("\n✅ Análise finalizada.")

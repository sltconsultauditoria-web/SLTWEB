import ast
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent.parent
ROUTERS_DIR = BASE_DIR / "routers"

print("\n🔎 CONSULT SLT ENTERPRISE - AUDITORIA DE ROTAS\n")
print("Diretório:", ROUTERS_DIR, "\n")

routers = []
routes = []
duplicates = defaultdict(list)

# ==========================================
# LER ROUTERS
# ==========================================

for file in ROUTERS_DIR.glob("*.py"):

    if file.name == "__init__.py":
        continue

    router_name = file.stem
    content = file.read_text(encoding="utf-8")

    tree = ast.parse(content)

    prefix = None

    for node in ast.walk(tree):

        if isinstance(node, ast.Assign):

            if isinstance(node.value, ast.Call):

                if getattr(node.value.func, "id", "") == "APIRouter":

                    for kw in node.value.keywords:

                        if kw.arg == "prefix":
                            prefix = kw.value.value

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

                        routes.append({
                            "router": router_name,
                            "method": method,
                            "path": path
                        })

    routers.append({
        "router": router_name,
        "prefix": prefix
    })

# ==========================================
# RELATORIO ROUTERS
# ==========================================

print("📦 ROUTERS DETECTADOS\n")

for r in routers:

    print("Router:", r["router"])

    if r["prefix"]:
        print("  ⚠ Prefix interno:", r["prefix"])
    else:
        print("  ✅ Sem prefix")

print("\n---------------------------------\n")

# ==========================================
# ANALISAR ROTAS
# ==========================================

for r in routes:

    router = r["router"]
    method = r["method"]
    path = r["path"]

    full = f"/api/{router}{path}"

    key = f"{method} {full}"

    duplicates[key].append(router)

# ==========================================
# DUPLICADOS
# ==========================================

print("❌ ENDPOINTS DUPLICADOS\n")

found = False

for route, routers_list in duplicates.items():

    if len(routers_list) > 1:

        found = True
        print(route)
        print("Routers:", routers_list)

if not found:
    print("Nenhum endpoint duplicado")

print("\n---------------------------------\n")

# ==========================================
# PREFIX DUPLICADO
# ==========================================

print("⚠ VERIFICANDO PREFIXOS DUPLICADOS\n")

prefix_problem = False

for r in routes:

    router = r["router"]
    path = r["path"]

    if f"/{router}/{router}" in f"/{router}{path}":

        prefix_problem = True
        print(f"/api/{router}{path}")

if not prefix_problem:
    print("Nenhum problema de prefix")

print("\n---------------------------------\n")

print("📊 ESTATÍSTICAS\n")

print("Routers:", len(routers))
print("Endpoints:", len(routes))

unique = set()

for r in routes:
    unique.add(f"{r['method']} {r['router']} {r['path']}")

print("Endpoints únicos:", len(unique))

print("\n🏁 Auditoria finalizada\n")
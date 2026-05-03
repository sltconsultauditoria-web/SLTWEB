# diagnostico_backend_frontend.py
# OBJETIVO:
# Varre frontend + backend e identifica:
# 1. Rotas chamadas no React (axios/fetch)
# 2. Rotas existentes no FastAPI
# 3. Quais endpoints faltam
# 4. Variáveis undefined (API_URL, VITE_API_URL etc)
# 5. Sugere correção automática

import os
import re
from pathlib import Path

BASE_DIR = r"C:\Users\admin-local\ServerApp\consultSLTweb"

FRONTEND = os.path.join(BASE_DIR, "frontend")
BACKEND = os.path.join(BASE_DIR, "backend")

print("=" * 70)
print("DIAGNÓSTICO FRONTEND x BACKEND")
print("=" * 70)

# ======================================================
# CAPTURAR ROTAS FRONTEND
# ======================================================

frontend_routes = []
env_vars = set()

patterns = [
    r'axios\.get\(["\']([^"\']+)["\']',
    r'axios\.post\(["\']([^"\']+)["\']',
    r'api\.get\(["\']([^"\']+)["\']',
    r'api\.post\(["\']([^"\']+)["\']',
    r'fetch\(["\']([^"\']+)["\']',
]

for root, dirs, files in os.walk(FRONTEND):
    for file in files:
        if file.endswith((".js", ".jsx", ".ts", ".tsx")):
            path = os.path.join(root, file)

            try:
                content = open(path, encoding="utf-8").read()
            except:
                continue

            # capturar rotas
            for p in patterns:
                matches = re.findall(p, content)
                for m in matches:
                    frontend_routes.append((file, m))

            # capturar env vars
            vars_found = re.findall(r'import\.meta\.env\.([A-Z0-9_]+)', content)
            for v in vars_found:
                env_vars.add(v)

# ======================================================
# CAPTURAR ROTAS BACKEND FASTAPI
# ======================================================

backend_routes = []

route_patterns = [
    r'@app\.get\(["\']([^"\']+)["\']',
    r'@app\.post\(["\']([^"\']+)["\']',
    r'@router\.get\(["\']([^"\']+)["\']',
    r'@router\.post\(["\']([^"\']+)["\']',
    r'include_router\(.+prefix=["\']([^"\']+)["\']'
]

for root, dirs, files in os.walk(BACKEND):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)

            try:
                content = open(path, encoding="utf-8").read()
            except:
                continue

            for p in route_patterns:
                matches = re.findall(p, content)
                for m in matches:
                    backend_routes.append((file, m))

# ======================================================
# NORMALIZAÇÃO
# ======================================================

def norm(url):
    return url.strip().replace("//", "/").rstrip("/")

frontend_clean = sorted(set([norm(x[1]) for x in frontend_routes]))
backend_clean = sorted(set([norm(x[1]) for x in backend_routes]))

# ======================================================
# RESULTADOS
# ======================================================

print("\nROTAS CHAMADAS NO FRONTEND:")
for r in frontend_clean:
    print("  ", r)

print("\nROTAS EXISTENTES NO BACKEND:")
for r in backend_clean:
    print("  ", r)

# ======================================================
# FALTANDO
# ======================================================

print("\n" + "=" * 70)
print("ENDPOINTS FALTANDO")
print("=" * 70)

faltando = []

for rota in frontend_clean:
    ok = False

    for b in backend_clean:
        if rota == b or rota.startswith(b) or b.startswith(rota):
            ok = True
            break

    if not ok:
        faltando.append(rota)
        print("❌", rota)

# ======================================================
# ENV VARS
# ======================================================

print("\n" + "=" * 70)
print("VARIÁVEIS DE AMBIENTE")
print("=" * 70)

for v in env_vars:
    print("Encontrada:", v)

env_file = os.path.join(FRONTEND, ".env")

if os.path.exists(env_file):
    env_content = open(env_file, encoding="utf-8").read()

    for v in env_vars:
        if v not in env_content:
            print("❌ Faltando no .env:", v)
else:
    print("❌ Arquivo .env não existe")

# ======================================================
# RELATÓRIO FINAL
# ======================================================

print("\n" + "=" * 70)
print("RESUMO")
print("=" * 70)

if faltando:
    print("Endpoints que precisam existir no backend:")
    for f in faltando:
        print("  ->", f)
else:
    print("✅ Nenhum endpoint faltando")

print("\nSe aparecer /undefined/api/... então falta variável .env")

print("""
Sugestão .env:

VITE_API_URL=http://localhost:8000
""")

print("=" * 70)
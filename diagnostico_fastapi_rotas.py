# diagnostico_fastapi_rotas.py
# Script completo para descobrir por que /auth/login e /dashboard retornam 404
# Execute dentro da pasta do projeto:
# python diagnostico_fastapi_rotas.py

import os
import re
import sys
import json
import importlib.util
from pathlib import Path

print("=" * 80)
print("DIAGNÓSTICO FASTAPI - ROTAS 404")
print("=" * 80)

BASE_DIR = Path.cwd()
print(f"📂 Pasta atual: {BASE_DIR}")

# ---------------------------------------------------
# 1. Procurar arquivos python principais
# ---------------------------------------------------
print("\n[1] Procurando arquivos principais...")

arquivos = []
for root, dirs, files in os.walk(BASE_DIR):
    for file in files:
        if file.endswith(".py"):
            arquivos.append(os.path.join(root, file))

for a in arquivos[:50]:
    print(" -", a)

# ---------------------------------------------------
# 2. Procurar FastAPI()
# ---------------------------------------------------
print("\n[2] Procurando app = FastAPI()")

apps = []

for arq in arquivos:
    try:
        txt = open(arq, encoding="utf-8").read()
        if "FastAPI(" in txt:
            apps.append(arq)
    except:
        pass

for x in apps:
    print("✅", x)

# ---------------------------------------------------
# 3. Procurar include_router
# ---------------------------------------------------
print("\n[3] Procurando include_router(...)")

for arq in arquivos:
    try:
        txt = open(arq, encoding="utf-8").read()
        if "include_router(" in txt:
            print(f"\n📄 {arq}")
            linhas = txt.splitlines()
            for i, l in enumerate(linhas, 1):
                if "include_router(" in l:
                    print(f"   Linha {i}: {l.strip()}")
    except:
        pass

# ---------------------------------------------------
# 4. Procurar @router.post("/login")
# ---------------------------------------------------
print("\n[4] Procurando rotas login/dashboard")

padroes = [
    "/login",
    "/auth/login",
    "/dashboard",
]

for arq in arquivos:
    try:
        txt = open(arq, encoding="utf-8").read()
        achou = False
        for p in padroes:
            if p in txt:
                if not achou:
                    print(f"\n📄 {arq}")
                    achou = True
                print("   contém:", p)
    except:
        pass

# ---------------------------------------------------
# 5. Testar import do main.py
# ---------------------------------------------------
print("\n[5] Testando import do app principal")

candidatos = [
    "main.py",
    "app.py",
    "backend/main.py",
    "backend/app.py",
]

encontrado = None

for c in candidatos:
    p = BASE_DIR / c
    if p.exists():
        encontrado = p
        break

if encontrado:
    print("✅ Arquivo principal:", encontrado)

    try:
        spec = importlib.util.spec_from_file_location("mainmod", encontrado)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        app = getattr(mod, "app", None)

        if app:
            print("✅ app carregado com sucesso")
            print("\nROTAS REGISTRADAS:\n")

            for r in app.routes:
                methods = getattr(r, "methods", [])
                print(f"{list(methods)} -> {r.path}")

        else:
            print("❌ variável app não encontrada")

    except Exception as e:
        print("❌ erro ao importar:", str(e))

else:
    print("❌ main.py não localizado")

# ---------------------------------------------------
# 6. Sugestões automáticas
# ---------------------------------------------------
print("\n[6] POSSÍVEIS CAUSAS DO 404")
print("""
1. Router auth.py não foi incluído no main.py

   app.include_router(auth_router)

2. Prefix errado

   router = APIRouter(prefix="/api")

   então rota vira:
   /api/auth/login

3. Arquivo errado sendo executado

   uvicorn backend.main:app --reload

4. Nome app diferente

   application = FastAPI()

5. Login existe como GET e não POST

6. include_router comentado
""")

print("=" * 80)
print("FIM")
print("=" * 80)
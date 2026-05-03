# validar_patch_final_consultsltweb.py
# Executar após reiniciar backend/frontend
# Objetivo: confirmar se o patch final foi realmente aplicado

import os
import re
import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\admin-local\ServerApp\consultSLTweb")
FRONTEND = BASE_DIR / "frontend"
BACKEND = BASE_DIR / "backend"

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

resultado = {
    "data": str(datetime.now()),
    "checks": {},
    "score": 0,
    "erros": [],
    "status": ""
}

print("=" * 100)
print("VALIDAÇÃO FINAL CONSULTSLTWEB")
print("=" * 100)

# ---------------------------------------------------
# FUNÇÃO AUXILIAR
# ---------------------------------------------------
def ok(nome, status, detalhe=""):
    resultado["checks"][nome] = {"ok": status, "detalhe": detalhe}
    print(f'{"✅" if status else "❌"} {nome} {detalhe}')

# ---------------------------------------------------
# 1. VERIFICAR Dashboard.jsx
# ---------------------------------------------------
print("\n[1] VALIDANDO DASHBOARD")

dashboard = FRONTEND / "src" / "pages" / "Dashboard.jsx"

if dashboard.exists():
    txt = dashboard.read_text(encoding="utf-8", errors="ignore")

    hardcoded = "/api/api/dashboard" in txt
    api_duplo = "api/api" in txt

    if not hardcoded and not api_duplo:
        ok("Dashboard sem /api/api", True)
    else:
        ok("Dashboard sem /api/api", False, "Ainda existe rota duplicada")
        resultado["erros"].append("Dashboard ainda usa /api/api")
else:
    ok("Dashboard.jsx existe", False)
    resultado["erros"].append("Dashboard.jsx ausente")

# ---------------------------------------------------
# 2. TESTAR BACKEND
# ---------------------------------------------------
print("\n[2] TESTANDO BACKEND")

rotas = [
    "/health",
    "/api/dashboard",
    "/api/alertas",
    "/api/obrigacoes"
]

for rota in rotas:
    try:
        r = requests.get(BACKEND_URL + rota, timeout=5)
        ok(rota, r.status_code == 200, f"-> {r.status_code}")
        if r.status_code != 200:
            resultado["erros"].append(f"{rota} retornou {r.status_code}")
    except Exception as e:
        ok(rota, False, f"-> {str(e)}")
        resultado["erros"].append(f"{rota} offline")

# ---------------------------------------------------
# 3. LOGIN
# ---------------------------------------------------
print("\n[3] TESTANDO LOGIN")

usuarios = [
    {"email": "admin@empresa.com", "password": "admin123"},
    {"email": "william.lucas@sltconsult.com.br", "password": "Slt@2024"},
    {"email": "admin@consultslt.com.br", "password": "Consult@2026"},
]

login_ok = 0

for u in usuarios:
    try:
        r = requests.post(
            BACKEND_URL + "/api/auth/login",
            json=u,
            timeout=5
        )

        if r.status_code in [200, 201]:
            login_ok += 1

    except:
        pass

ok("Login usuários padrão", login_ok >= 1, f"{login_ok}/3 funcionando")

if login_ok == 0:
    resultado["erros"].append("Nenhum login funcionou")

# ---------------------------------------------------
# 4. FRONTEND ONLINE
# ---------------------------------------------------
print("\n[4] TESTANDO FRONTEND")

try:
    r = requests.get(FRONTEND_URL, timeout=5)
    ok("Frontend online", r.status_code in [200, 304], f"-> {r.status_code}")
except:
    ok("Frontend online", False)
    resultado["erros"].append("Frontend offline")

# ---------------------------------------------------
# SCORE
# ---------------------------------------------------
total = len(resultado["checks"])
success = len([x for x in resultado["checks"].values() if x["ok"]])

score = int((success / total) * 100) if total else 0
resultado["score"] = score

if score >= 95:
    status = "SISTEMA TOTALMENTE FUNCIONAL"
elif score >= 80:
    status = "SISTEMA ESTÁVEL COM PEQUENOS AJUSTES"
else:
    status = "AINDA REQUER CORREÇÕES"

resultado["status"] = status

# ---------------------------------------------------
# SALVAR
# ---------------------------------------------------
arquivo = BASE_DIR / "relatorio_validacao_final.json"
arquivo.write_text(json.dumps(resultado, indent=4, ensure_ascii=False), encoding="utf-8")

print("\n" + "=" * 100)
print("RESULTADO FINAL")
print("=" * 100)
print(f"Score: {score}/100")
print(status)

if resultado["erros"]:
    print("\nERROS:")
    for e in resultado["erros"]:
        print(" -", e)

print(f"\nRelatório salvo em:\n{arquivo}")
print("=" * 100)
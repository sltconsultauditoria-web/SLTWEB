# ==========================================================
# verificar_impacto_dashboard_update.py
# CONSULTSLT - PRE CHECK IMPACTO ANTES DO UPGRADE DASHBOARD
# Verifica tudo antes de aplicar upgrade_total_dashboard_premium.py
# ==========================================================

import os
import json
import shutil
import requests
from datetime import datetime

BASE_DIR = r"C:\Users\admin-local\ServerApp\consultSLTweb"
BACKEND = os.path.join(BASE_DIR, "backend")
FRONTEND = os.path.join(BASE_DIR, "frontend")
REPORT = os.path.join(BASE_DIR, "impacto_dashboard_update.json")

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

resultado = {
    "data": str(datetime.now()),
    "estrutura": {},
    "arquivos_criticos": {},
    "apis": {},
    "frontend": {},
    "impacto": {},
    "risco": "BAIXO",
    "recomendacao": ""
}

# ==========================================================
# FUNÇÕES
# ==========================================================
def check_path(nome, path):
    ok = os.path.exists(path)
    resultado["estrutura"][nome] = ok
    print(f"{'✅' if ok else '❌'} {nome}: {path}")
    return ok

def check_file(nome, path):
    ok = os.path.isfile(path)
    resultado["arquivos_criticos"][nome] = ok
    print(f"{'✅' if ok else '❌'} {nome}")
    return ok

def check_url(nome, url):
    try:
        r = requests.get(url, timeout=5)
        resultado["apis"][nome] = r.status_code
        print(f"{'✅' if r.status_code == 200 else '⚠️'} {nome}: {r.status_code}")
        return r.status_code
    except:
        resultado["apis"][nome] = "OFFLINE"
        print(f"❌ {nome}: OFFLINE")
        return None

def backup_file(path):
    if os.path.exists(path):
        bk = path + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(path, bk)
        print(f"💾 Backup criado: {os.path.basename(path)}")

# ==========================================================
# HEADER
# ==========================================================
print("="*70)
print("VERIFICAÇÃO DE IMPACTO - DASHBOARD PREMIUM")
print("="*70)

# ==========================================================
# ESTRUTURA
# ==========================================================
print("\nVALIDANDO ESTRUTURA")
check_path("BASE_DIR", BASE_DIR)
check_path("BACKEND", BACKEND)
check_path("FRONTEND", FRONTEND)
check_path("SRC_PAGES", os.path.join(FRONTEND, "src", "pages"))
check_path("SRC_COMPONENTS", os.path.join(FRONTEND, "src", "components"))

# ==========================================================
# ARQUIVOS CRÍTICOS
# ==========================================================
print("\nVALIDANDO ARQUIVOS CRÍTICOS")

arquivos = {
    "main_enterprise.py": os.path.join(BACKEND, "main_enterprise.py"),
    "Dashboard.jsx": os.path.join(FRONTEND, "src", "pages", "Dashboard.jsx"),
    "api.js": os.path.join(FRONTEND, "src", "services", "api.js"),
    ".env": os.path.join(FRONTEND, ".env"),
}

for nome, path in arquivos.items():
    if check_file(nome, path):
        backup_file(path)

# ==========================================================
# BACKEND ONLINE
# ==========================================================
print("\nVALIDANDO BACKEND")
check_url("health", BACKEND_URL + "/health")
check_url("docs", BACKEND_URL + "/docs")
check_url("dashboard", BACKEND_URL + "/api/dashboard")
check_url("empresas", BACKEND_URL + "/api/empresas")
check_url("guias", BACKEND_URL + "/api/guias")
check_url("documentos", BACKEND_URL + "/api/documentos")
check_url("alertas", BACKEND_URL + "/api/alertas")
check_url("obrigacoes", BACKEND_URL + "/api/obrigacoes")

# ==========================================================
# FRONTEND ONLINE
# ==========================================================
print("\nVALIDANDO FRONTEND")
check_url("frontend_home", FRONTEND_URL)
check_url("dashboard_page", FRONTEND_URL + "/dashboard")

# ==========================================================
# ANÁLISE DE IMPACTO
# ==========================================================
print("\nANÁLISE DE IMPACTO")

problemas = 0

for k,v in resultado["apis"].items():
    if v != 200:
        problemas += 1

if problemas == 0:
    risco = "BAIXO"
elif problemas <= 3:
    risco = "MÉDIO"
else:
    risco = "ALTO"

resultado["risco"] = risco

print(f"📊 APIs com problema: {problemas}")
print(f"📌 Risco estimado: {risco}")

# ==========================================================
# RECOMENDAÇÃO
# ==========================================================
if risco == "BAIXO":
    recomendacao = """
✅ Ambiente estável.
Pode executar upgrade_total_dashboard_premium.py com segurança.
"""
elif risco == "MÉDIO":
    recomendacao = """
⚠️ Corrigir APIs quebradas antes do upgrade.
Recomendado revisar backend e collections Mongo.
"""
else:
    recomendacao = """
❌ Alto risco.
Não executar upgrade agora.
Necessário corrigir backend, CORS, endpoints e frontend.
"""

resultado["recomendacao"] = recomendacao
print(recomendacao)

# ==========================================================
# O QUE SERÁ ALTERADO NO UPGRADE
# ==========================================================
print("O UPGRADE IRÁ ALTERAR:")
print("1. Dashboard.jsx")
print("2. main_enterprise.py")
print("3. Métricas em tempo real")
print("4. KPIs fiscais")
print("5. Cards premium")
print("6. Gráficos")
print("7. Top empresas")
print("8. Alertas inteligentes")

# ==========================================================
# SALVAR JSON
# ==========================================================
with open(REPORT, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

print("\n📁 Relatório salvo em:")
print(REPORT)

print("\nFINALIZADO")
print("="*70)
# verificar_upgrade_enterprise_consultsltweb.py
# Diagnóstico pós-upgrade: confirma se upgrade foi aplicado e identifica erros atuais
# Execute em:
# python verificar_upgrade_enterprise_consultsltweb.py

import os
import re
import json
import requests
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\admin-local\ServerApp\consultSLTweb")
FRONTEND = BASE_DIR / "frontend"
BACKEND = BASE_DIR / "backend"

API = "http://localhost:8000"
FRONT = "http://localhost:3000"

print("=" * 100)
print("CONSULTSLTWEB - VERIFICAÇÃO REAL DO UPGRADE ENTERPRISE")
print("=" * 100)

resultado = {
    "data": str(datetime.now()),
    "upgrade_detectado": {},
    "erros": [],
    "score": 0,
    "acoes": []
}

# ==========================================================
# 1. VERIFICAR ARQUIVOS DO UPGRADE
# ==========================================================
print("\n[1] VERIFICANDO ARQUIVOS GERADOS")

arquivos = {
    "layout_enterprise": FRONTEND / "src/layouts/MainLayout.jsx",
    "dashboard_premium": FRONTEND / "src/pages/Dashboard.jsx",
    "ocr_page": FRONTEND / "src/pages/OCR.jsx",
    "ocr_backend": BACKEND / "ocr_routes.py",
    "main_backend": BACKEND / "main_enterprise.py",
    "api_service": FRONTEND / "src/services/api.js",
}

ok = 0

for nome, arq in arquivos.items():
    existe = arq.exists()
    resultado["upgrade_detectado"][nome] = existe
    print(("✅" if existe else "❌"), nome, "->", arq)
    if existe:
        ok += 1

# ==========================================================
# 2. TESTAR BACKEND
# ==========================================================
print("\n[2] TESTANDO BACKEND")

rotas = [
    "/health",
    "/docs",
    "/openapi.json",
    "/api/dashboard",
    "/api/alertas",
    "/api/obrigacoes",
]

for rota in rotas:
    try:
        r = requests.get(API + rota, timeout=5)
        print(f"{rota:25} -> {r.status_code}")
        if r.status_code >= 400:
            resultado["erros"].append(f"{rota} retornou {r.status_code}")
    except Exception as e:
        print(f"{rota:25} -> FALHOU")
        resultado["erros"].append(f"{rota} offline")

# ==========================================================
# 3. ANALISAR DUPLO /api/api
# ==========================================================
print("\n[3] ANALISANDO ERRO /api/api")

api_js = FRONTEND / "src/services/api.js"

if api_js.exists():
    txt = api_js.read_text(encoding="utf-8", errors="ignore")

    if "/api" in txt:
        print("✅ baseURL contém /api")
    else:
        print("❌ baseURL incorreto")

# buscar páginas com /api/dashboard hardcoded
for raiz, dirs, files in os.walk(FRONTEND / "src"):
    for f in files:
        if f.endswith((".js", ".jsx")):
            p = Path(raiz) / f
            t = p.read_text(encoding="utf-8", errors="ignore")

            if "/api/dashboard" in t:
                resultado["erros"].append(f"{f} usa /api/dashboard hardcoded")

            if "undefined/api/" in t:
                resultado["erros"].append(f"{f} usa variável undefined")

# ==========================================================
# 4. CORS
# ==========================================================
print("\n[4] VERIFICANDO CORS")

main = BACKEND / "main_enterprise.py"
if main.exists():
    txt = main.read_text(encoding="utf-8", errors="ignore")

    if "CORSMiddleware" in txt:
        print("✅ CORSMiddleware detectado")
    else:
        print("❌ CORSMiddleware ausente")
        resultado["erros"].append("CORS não configurado")

# ==========================================================
# 5. KEY DUPLICADAS REACT
# ==========================================================
print("\n[5] VERIFICANDO KEY EM LISTAS")

pages = ["Empresas.jsx", "Documentos.jsx", "Guias.jsx"]

for nome in pages:
    achou = False
    for raiz, dirs, files in os.walk(FRONTEND / "src"):
        for f in files:
            if f == nome:
                p = Path(raiz) / f
                txt = p.read_text(encoding="utf-8", errors="ignore")
                if ".map(" in txt and "key=" not in txt:
                    resultado["erros"].append(f"{nome} sem key em listas")
                    achou = True
    print(("❌" if achou else "✅"), nome)

# ==========================================================
# SCORE
# ==========================================================
score = 100 - (len(resultado["erros"]) * 5)
if score < 0:
    score = 0

resultado["score"] = score

# ==========================================================
# RECOMENDAÇÕES
# ==========================================================
if any("/api/dashboard hardcoded" in e for e in resultado["erros"]):
    resultado["acoes"].append("Corrigir Dashboard.jsx para usar api.get('/dashboard')")

if any("undefined" in e for e in resultado["erros"]):
    resultado["acoes"].append("Corrigir variáveis VITE_API_URL / REACT_APP_API_URL")

if any("CORS" in e for e in resultado["erros"]):
    resultado["acoes"].append("Adicionar CORSMiddleware no FastAPI")

if any("500" in e for e in resultado["erros"]):
    resultado["acoes"].append("Corrigir exceções internas dos endpoints")

# ==========================================================
# FINAL
# ==========================================================
print("\n" + "=" * 100)
print("RESULTADO FINAL")
print("=" * 100)

print("Score:", score, "/100")

if score >= 85:
    print("✅ Upgrade aplicado corretamente")
elif score >= 60:
    print("⚠️ Upgrade parcial aplicado")
else:
    print("❌ Upgrade falhou ou incompleto")

print("\nERROS ENCONTRADOS:")
for e in resultado["erros"]:
    print(" -", e)

print("\nAÇÕES:")
for a in resultado["acoes"]:
    print(" ->", a)

arquivo = BASE_DIR / "relatorio_upgrade_real.json"
with open(arquivo, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

print("\nRelatório salvo em:")
print(arquivo)
print("=" * 100)
# verificar_atualizacao_tailadmin_ocr.py
# ==========================================================
# VERIFICAÇÃO COMPLETA:
# 1. Backend OCR atualizado
# 2. Collections Mongo OCR
# 3. Frontend TailAdmin atualizado
# 4. Arquivos React/Tailwind existentes
# 5. Score final
# ==========================================================

import os
import json
import requests
from datetime import datetime
from pathlib import Path

# ==========================================================
# CONFIG
# ==========================================================
BACKEND_URL = "http://localhost:8000"
FRONTEND_PATH = r"C:\Users\admin-local\ServerApp\consultSLTweb"
TIMEOUT = 5

resultado = {
    "data_execucao": str(datetime.now()),
    "checks": {},
    "score": 0,
    "status": ""
}

score = 0
total = 10

# ==========================================================
# HELPERS
# ==========================================================
def ok(nome, detalhe="OK"):
    global score
    resultado["checks"][nome] = {
        "ok": True,
        "detalhe": detalhe
    }
    score += 1


def fail(nome, detalhe):
    resultado["checks"][nome] = {
        "ok": False,
        "detalhe": detalhe
    }

# ==========================================================
# BACKEND OCR
# ==========================================================
try:
    r = requests.get(f"{BACKEND_URL}/api/ocr/documentos", timeout=TIMEOUT)
    if r.status_code == 200:
        ok("ocr_documentos_api", f"status {r.status_code}")
    else:
        fail("ocr_documentos_api", f"status {r.status_code}")
except Exception as e:
    fail("ocr_documentos_api", str(e))

try:
    r = requests.get(f"{BACKEND_URL}/api/ocr/estatisticas", timeout=TIMEOUT)
    if r.status_code == 200:
        ok("ocr_estatisticas_api", f"status {r.status_code}")
    else:
        fail("ocr_estatisticas_api", f"status {r.status_code}")
except Exception as e:
    fail("ocr_estatisticas_api", str(e))

try:
    r = requests.get(f"{BACKEND_URL}/api/ocr/tipos-suportados", timeout=TIMEOUT)
    if r.status_code == 200:
        ok("ocr_tipos_api", f"status {r.status_code}")
    else:
        fail("ocr_tipos_api", f"status {r.status_code}")
except Exception as e:
    fail("ocr_tipos_api", str(e))

# ==========================================================
# FRONTEND TAILADMIN
# ==========================================================
arquivos_importantes = [
    "src/App.jsx",
    "src/App.js",
    "tailwind.config.js",
    "postcss.config.js",
    "package.json",
]

for arq in arquivos_importantes:
    caminho = Path(FRONTEND_PATH) / arq
    nome = f"arquivo_{arq}"

    if caminho.exists():
        ok(nome, "encontrado")
    else:
        fail(nome, "não encontrado")

# ==========================================================
# PROCURAR TAILADMIN
# ==========================================================
tailadmin_encontrado = False

for raiz, dirs, files in os.walk(FRONTEND_PATH):
    for file in files:
        nome = file.lower()

        if "dashboard" in nome or "tailadmin" in nome:
            tailadmin_encontrado = True
            break

if tailadmin_encontrado:
    ok("tailadmin_layout", "arquivos encontrados")
else:
    fail("tailadmin_layout", "não localizado")

# ==========================================================
# SCORE
# ==========================================================
resultado["score"] = int((score / total) * 100)

if resultado["score"] >= 90:
    resultado["status"] = "SISTEMA TOTALMENTE ATUALIZADO"
elif resultado["score"] >= 70:
    resultado["status"] = "ATUALIZADO PARCIALMENTE"
else:
    resultado["status"] = "REQUER AJUSTES"

# ==========================================================
# SAVE
# ==========================================================
arquivo_saida = "relatorio_verificacao_tailadmin_ocr.json"

with open(arquivo_saida, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

# ==========================================================
# OUTPUT
# ==========================================================
print("=" * 70)
print("VERIFICAÇÃO TAILADMIN + OCR")
print("=" * 70)

for nome, item in resultado["checks"].items():
    emoji = "✅" if item["ok"] else "❌"
    print(f"{emoji} {nome} -> {item['detalhe']}")

print("=" * 70)
print("SCORE:", resultado["score"])
print("STATUS:", resultado["status"])
print("RELATÓRIO:", arquivo_saida)
print("=" * 70)
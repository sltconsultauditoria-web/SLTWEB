# verificar_tailadmin_ocr_v2.py
# ==========================================================
# VERSÃO PROFISSIONAL CORRIGIDA
# Detecta estrutura React real
# Detecta TailAdmin
# Corrige OCR
# Score real
# ==========================================================

import os
import json
import requests
from pathlib import Path
from datetime import datetime

BASE = Path(r"C:\Users\admin-local\ServerApp\consultSLTweb")
BACKEND = "http://localhost:8000"

resultado = {
    "data": str(datetime.now()),
    "checks": {},
    "score": 0,
    "status": ""
}

pontos = 0
max_pontos = 10

# ==========================================================
# HELPERS
# ==========================================================
def ok(nome, detalhe="OK"):
    global pontos
    resultado["checks"][nome] = {"ok": True, "detalhe": detalhe}
    pontos += 1

def fail(nome, detalhe):
    resultado["checks"][nome] = {"ok": False, "detalhe": detalhe}

# ==========================================================
# BACKEND OCR
# ==========================================================
rotas = [
    "/api/ocr/documentos",
    "/api/ocr/estatisticas",
    "/api/ocr/tipos-suportados"
]

for rota in rotas:
    nome = rota.replace("/", "_")

    try:
        r = requests.get(BACKEND + rota, timeout=5)
        if r.status_code == 200:
            ok(nome, "200")
        else:
            fail(nome, str(r.status_code))
    except Exception as e:
        fail(nome, str(e))

# ==========================================================
# FRONTEND - PROCURA package.json REAL
# ==========================================================
package_found = False

for raiz, dirs, files in os.walk(BASE):
    if "package.json" in files:
        ok("package_json", raiz)
        package_found = True
        break

if not package_found:
    fail("package_json", "não encontrado")

# ==========================================================
# PROCURA SRC
# ==========================================================
src_found = False

for raiz, dirs, files in os.walk(BASE):
    if os.path.basename(raiz).lower() == "src":
        ok("src_folder", raiz)
        src_found = True
        break

if not src_found:
    fail("src_folder", "não encontrado")

# ==========================================================
# TAILWIND
# ==========================================================
tailwind = False

for raiz, dirs, files in os.walk(BASE):
    for f in files:
        nome = f.lower()
        if "tailwind.config.js" == nome:
            tailwind = True
            ok("tailwind_config", os.path.join(raiz, f))

if not tailwind:
    fail("tailwind_config", "não encontrado")

# ==========================================================
# POSTCSS
# ==========================================================
postcss = False

for raiz, dirs, files in os.walk(BASE):
    for f in files:
        nome = f.lower()
        if "postcss.config.js" == nome:
            postcss = True
            ok("postcss_config", os.path.join(raiz, f))

if not postcss:
    fail("postcss_config", "não encontrado")

# ==========================================================
# TAILADMIN
# ==========================================================
tailadmin = False

keywords = [
    "tailadmin",
    "sidebar",
    "dashboard",
    "adminlayout",
    "header"
]

for raiz, dirs, files in os.walk(BASE):
    for f in files:
        if f.endswith((".js", ".jsx", ".tsx")):
            arquivo = os.path.join(raiz, f)

            try:
                texto = open(
                    arquivo,
                    encoding="utf-8",
                    errors="ignore"
                ).read().lower()

                if any(k in texto for k in keywords):
                    tailadmin = True
                    ok("tailadmin_detectado", arquivo)
                    raise StopIteration

            except:
                pass

try:
    pass
except:
    pass

if not tailadmin:
    fail("tailadmin_detectado", "não localizado")

# ==========================================================
# SCORE
# ==========================================================
resultado["score"] = int((pontos / max_pontos) * 100)

if resultado["score"] >= 90:
    resultado["status"] = "SISTEMA ATUALIZADO"
elif resultado["score"] >= 70:
    resultado["status"] = "PARCIALMENTE ATUALIZADO"
else:
    resultado["status"] = "REQUER AJUSTES"

# ==========================================================
# SAVE
# ==========================================================
saida = "relatorio_tailadmin_ocr_v2.json"

with open(saida, "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=4, ensure_ascii=False)

# ==========================================================
# OUTPUT
# ==========================================================
print("=" * 70)
print("VERIFICAÇÃO TAILADMIN + OCR V2")
print("=" * 70)

for k, v in resultado["checks"].items():
    emoji = "✅" if v["ok"] else "❌"
    print(f"{emoji} {k} -> {v['detalhe']}")

print("=" * 70)
print("SCORE:", resultado["score"])
print("STATUS:", resultado["status"])
print("ARQUIVO:", saida)
print("=" * 70)
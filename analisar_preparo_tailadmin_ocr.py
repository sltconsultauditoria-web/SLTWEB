# analisar_preparo_tailadmin_ocr.py
# ==========================================================
# CONSULTSLTWEB - ANÁLISE DE PREPARO PARA TAILADMIN + OCR
# Verifica se a aplicação está pronta para upgrade sem quebrar nada
# ==========================================================

import os
import json
import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path.cwd()
FRONTEND = BASE_DIR / "frontend"
BACKEND = BASE_DIR / "backend"

RELATORIO = {
    "data": str(datetime.now()),
    "estrutura": {},
    "frontend": {},
    "backend": {},
    "mongodb": {},
    "score": {},
    "acoes_recomendadas": []
}

print("=" * 90)
print("ANÁLISE DE PREPARO - TAILADMIN + OCR")
print("=" * 90)

# ==========================================================
# FUNÇÕES
# ==========================================================

def existe(p):
    return p.exists()

def contar_arquivos(pasta, extensao):
    total = 0
    if pasta.exists():
        for root, dirs, files in os.walk(pasta):
            for f in files:
                if f.endswith(extensao):
                    total += 1
    return total

def localizar_texto(pasta, texto):
    encontrados = []
    if not pasta.exists():
        return encontrados

    for root, dirs, files in os.walk(pasta):
        for f in files:
            if f.endswith((".js", ".jsx", ".ts", ".tsx", ".py")):
                arq = Path(root) / f
                try:
                    content = arq.read_text(encoding="utf-8", errors="ignore")
                    if texto.lower() in content.lower():
                        encontrados.append(str(arq))
                except:
                    pass
    return encontrados

# ==========================================================
# 1. ESTRUTURA
# ==========================================================

print("\n[1] VALIDANDO ESTRUTURA")

estrutura_ok = 0

for pasta in [FRONTEND, BACKEND]:
    nome = pasta.name
    status = existe(pasta)
    RELATORIO["estrutura"][nome] = status
    print(f"{'✅' if status else '❌'} {nome}")
    if status:
        estrutura_ok += 1

# ==========================================================
# 2. FRONTEND
# ==========================================================

print("\n[2] ANALISANDO FRONTEND")

package_json = FRONTEND / "package.json"
tailwind = FRONTEND / "tailwind.config.js"
src = FRONTEND / "src"

react_ok = False
tailwind_ok = False
axios_ok = False
router_ok = False

if package_json.exists():
    try:
        pkg = json.loads(package_json.read_text(encoding="utf-8"))
        deps = str(pkg)

        react_ok = "react" in deps.lower()
        tailwind_ok = "tailwind" in deps.lower()
        axios_ok = "axios" in deps.lower()
        router_ok = "react-router" in deps.lower()
    except:
        pass

paginas = contar_arquivos(src, ".jsx") + contar_arquivos(src, ".js")

print(f"{'✅' if react_ok else '❌'} React")
print(f"{'✅' if tailwind_ok else '❌'} Tailwind")
print(f"{'✅' if axios_ok else '❌'} Axios")
print(f"{'✅' if router_ok else '❌'} React Router")
print(f"✅ Telas encontradas: {paginas}")

RELATORIO["frontend"] = {
    "react": react_ok,
    "tailwind": tailwind_ok,
    "axios": axios_ok,
    "router": router_ok,
    "paginas": paginas
}

# ==========================================================
# 3. BACKEND
# ==========================================================

print("\n[3] ANALISANDO BACKEND")

fastapi = localizar_texto(BACKEND, "FastAPI(")
mongo = localizar_texto(BACKEND, "MongoClient")
jwt = localizar_texto(BACKEND, "jwt")
api_routes = localizar_texto(BACKEND, "@app.")

print(f"{'✅' if fastapi else '❌'} FastAPI detectado")
print(f"{'✅' if mongo else '❌'} MongoDB detectado")
print(f"{'✅' if jwt else '❌'} JWT/Login detectado")
print(f"✅ Rotas estimadas: {len(api_routes)}")

RELATORIO["backend"] = {
    "fastapi": bool(fastapi),
    "mongodb": bool(mongo),
    "jwt": bool(jwt),
    "rotas": len(api_routes)
}

# ==========================================================
# 4. PREPARO PARA TAILADMIN
# ==========================================================

print("\n[4] PREPARO PARA TAILADMIN")

tailadmin_score = 0

if react_ok:
    tailadmin_score += 30
if tailwind_ok:
    tailadmin_score += 30
if router_ok:
    tailadmin_score += 20
if paginas >= 5:
    tailadmin_score += 20

print(f"Score TailAdmin: {tailadmin_score}/100")

if tailadmin_score >= 80:
    print("✅ Aplicação pronta para upgrade visual")
elif tailadmin_score >= 50:
    print("⚠️ Precisa pequenos ajustes")
else:
    print("❌ Precisa estruturar frontend")

# ==========================================================
# 5. PREPARO PARA OCR
# ==========================================================

print("\n[5] PREPARO PARA OCR")

upload_detectado = localizar_texto(FRONTEND, "input type=\"file\"")
pdf_detectado = localizar_texto(BACKEND, "UploadFile")
pil_detectado = localizar_texto(BACKEND, "PIL")
cv_detectado = localizar_texto(BACKEND, "cv2")

ocr_score = 0

if mongo:
    ocr_score += 25
if pdf_detectado:
    ocr_score += 25
if upload_detectado:
    ocr_score += 25
if bool(fastapi):
    ocr_score += 25

print(f"Score OCR: {ocr_score}/100")

if ocr_score >= 75:
    print("✅ Aplicação pronta para OCR")
elif ocr_score >= 50:
    print("⚠️ Precisa poucos ajustes")
else:
    print("❌ Precisa criar base OCR")

# ==========================================================
# 6. O QUE PRECISA SER FEITO
# ==========================================================

print("\n[6] O QUE PRECISA SER FEITO")

acoes = []

if not tailwind_ok:
    acoes.append("Instalar TailwindCSS")

if not axios_ok:
    acoes.append("Centralizar APIs com Axios")

if paginas < 5:
    acoes.append("Organizar páginas React")

if not pdf_detectado:
    acoes.append("Criar endpoint upload FastAPI")

if not upload_detectado:
    acoes.append("Criar tela Upload Documentos")

acoes.append("Criar collection mongodb: ocr_documentos")
acoes.append("Instalar pytesseract + pdf2image")
acoes.append("Aplicar TailAdmin sem alterar rotas existentes")

for a in acoes:
    print("➡", a)

RELATORIO["acoes_recomendadas"] = acoes

# ==========================================================
# 7. SCORE FINAL
# ==========================================================

print("\n[7] RESULTADO FINAL")

score_final = int((tailadmin_score + ocr_score) / 2)

if score_final >= 80:
    status = "PRONTA PARA UPGRADE"
elif score_final >= 60:
    status = "BOA BASE - AJUSTES PEQUENOS"
else:
    status = "PRECISA ESTRUTURAÇÃO"

print(f"Score Geral: {score_final}/100")
print(f"Status: {status}")

RELATORIO["score"] = {
    "tailadmin": tailadmin_score,
    "ocr": ocr_score,
    "geral": score_final,
    "status": status
}

# ==========================================================
# SALVAR RELATÓRIO
# ==========================================================

saida = BASE_DIR / "relatorio_preparo_tailadmin_ocr.json"
with open(saida, "w", encoding="utf-8") as f:
    json.dump(RELATORIO, f, indent=4, ensure_ascii=False)

print("\n✅ Relatório salvo em:")
print(saida)

print("=" * 90)
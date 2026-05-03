# ==============================================================
# CORREÇÃO PYMONGO BOOL ERROR
# substituir verificar_correlacao_total.py completo
# ==============================================================

import os
import re
import json
import requests
from pymongo import MongoClient
from datetime import datetime

ROOT = r"C:\Users\admin-local\ServerApp\consultSLTweb"

FRONT = os.path.join(ROOT, "frontend", "src")
PAGES = os.path.join(FRONT, "pages")

API = "http://localhost:8000"
MONGO = "mongodb://localhost:27017"
DBNAME = "consultslt_db"

LOG_FILE = os.path.join(ROOT, "healthcheck_correlacao.json")


# ==============================================================
# HELPERS
# ==============================================================
def titulo(txt):
    print("\n" + "=" * 70)
    print(txt)
    print("=" * 70)


def ok(txt):
    print(f"✅ {txt}")


def erro(txt):
    print(f"❌ {txt}")


def alerta(txt):
    print(f"⚠️ {txt}")


# ==============================================================
# MONGO
# ==============================================================
def conectar_mongo():
    try:
        cli = MongoClient(MONGO, serverSelectionTimeoutMS=3000)
        cli.server_info()
        return cli[DBNAME]
    except Exception:
        return None


# ==============================================================
# COLLECTIONS
# ==============================================================
def listar_collections(db):
    titulo("COLEÇÕES MONGO")

    # CORREÇÃO AQUI
    if db is None:
        erro("Mongo offline")
        return {}

    dados = {}

    try:
        cols = db.list_collection_names()

        for c in cols:
            qtd = db[c].count_documents({})
            dados[c] = qtd
            ok(f"{c}: {qtd}")

    except Exception as e:
        erro(str(e))

    return dados


# ==============================================================
# ENDPOINTS
# ==============================================================
def listar_endpoints():
    titulo("ENDPOINTS BACKEND")

    try:
        r = requests.get(API + "/openapi.json", timeout=5)
        data = r.json()

        paths = data.get("paths", {})
        lista = sorted(paths.keys())

        for ep in lista:
            ok(ep)

        return lista

    except Exception:
        erro("Erro lendo OpenAPI")
        return []


# ==============================================================
# PAGES
# ==============================================================
def listar_pages():
    titulo("PAGES FRONTEND")

    if not os.path.exists(PAGES):
        erro("pages não encontrada")
        return []

    lista = []

    for arq in os.listdir(PAGES):
        if arq.endswith(".jsx") or arq.endswith(".js"):
            nome = arq.replace(".jsx", "").replace(".js", "")
            lista.append(nome)
            ok(nome)

    return lista


# ==============================================================
# MAPEAR API CALLS
# ==============================================================
def mapear_calls():
    titulo("MAPEANDO CHAMADAS")

    mapa = {}

    if not os.path.exists(PAGES):
        return mapa

    for arq in os.listdir(PAGES):

        if not arq.endswith((".jsx", ".js")):
            continue

        path = os.path.join(PAGES, arq)

        try:
            txt = open(path, encoding="utf-8").read()
        except:
            continue

        achados = re.findall(r'["\'](/api/[^"\']+)["\']', txt)

        if achados:
            mapa[arq] = list(set(achados))

        for item in achados:
            ok(f"{arq} -> {item}")

    return mapa


# ==============================================================
# CORRELAÇÃO
# ==============================================================
def correlacao(mapa, endpoints):
    titulo("CORRELAÇÃO PAGE x ENDPOINT")

    faltando = []

    for page, eps in mapa.items():
        for ep in eps:
            if ep in endpoints:
                ok(f"{page} -> {ep}")
            else:
                erro(f"{page} -> inexistente {ep}")
                faltando.append(ep)

    return faltando


# ==============================================================
# TESTE DADOS REAIS
# ==============================================================
def testar_dados():
    titulo("VALIDANDO DADOS REAIS")

    testes = [
        "/api/dashboard",
        "/api/empresas",
        "/api/documentos",
        "/api/guias",
        "/api/usuarios",
    ]

    for ep in testes:
        try:
            r = requests.get(API + ep, timeout=5)

            if r.status_code == 200:

                try:
                    js = r.json()

                    if isinstance(js, list):
                        ok(f"{ep}: {len(js)} registros")

                    elif isinstance(js, dict):
                        ok(f"{ep}: objeto")

                    else:
                        ok(f"{ep}: resposta")

                except:
                    ok(f"{ep}: texto")

            else:
                erro(f"{ep}: {r.status_code}")

        except:
            erro(ep)


# ==============================================================
# SUGESTÕES
# ==============================================================
def sugestoes(cols, faltando):
    titulo("O QUE FALTA")

    base = ["alertas", "auditoria", "obrigacoes"]

    for item in base:
        if item not in cols:
            alerta(f"Criar collection {item}")

    if faltando:
        alerta("Criar endpoints faltantes:")
        for x in sorted(set(faltando)):
            print("   ->", x)

    print("\nMelhorias:")
    print("1. Dashboard realtime")
    print("2. JWT")
    print("3. Logs")
    print("4. Robots scheduler")
    print("5. Redis cache")
    print("6. Error handler")
    print("7. Seeds Mongo")


# ==============================================================
# LOG
# ==============================================================
def salvar(cols, endpoints, pages):
    data = {
        "gerado_em": str(datetime.now()),
        "collections": cols,
        "endpoints": endpoints,
        "pages": pages,
    }

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    ok("healthcheck_correlacao.json salvo")


# ==============================================================
# MAIN
# ==============================================================
if __name__ == "__main__":

    titulo("CONSULTSLT CORRELAÇÃO TOTAL")

    db = conectar_mongo()

    cols = listar_collections(db)
    endpoints = listar_endpoints()
    pages = listar_pages()
    mapa = mapear_calls()

    faltando = correlacao(mapa, endpoints)

    testar_dados()

    sugestoes(cols, faltando)

    salvar(cols, endpoints, pages)

    titulo("FINALIZADO")
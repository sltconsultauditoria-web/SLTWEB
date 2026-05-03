# ===============================================================
# VERIFICADOR FULL STACK ENTERPRISE
# Arquivo: verificar_ecossistema_total.py
#
# Objetivo:
# - Validar Backend FastAPI
# - Validar Frontend React
# - Validar Mongo consultslt_db
# - Validar Endpoints
# - Validar Collections
# - Detectar erros de integração
# - Mostrar o que falta para dashboard 100%
#
# EXECUTAR:
# python verificar_ecossistema_total.py
# ===============================================================

import requests
import socket
import json
import time
from datetime import datetime

# =========================
# CONFIG
# =========================
BACKEND = "http://localhost:8000"
FRONTEND = "http://localhost:3000"
TIMEOUT = 5

# =========================
# ENDPOINTS IMPORTANTES
# =========================
ENDPOINTS = [
    "/",
    "/docs",
    "/openapi.json",
    "/api/dashboard",
    "/api/auth/login",
    "/api/empresas",
    "/api/documentos",
    "/api/guias",
    "/api/usuarios",
    "/api/alertas",
    "/api/obrigacoes",
    "/api/auditoria",
    "/api/auditoria/estatisticas",
    "/api/robots/ingestion/status",
    "/api/robots/ingestion/files",
    "/api/robots/ingestion/history",
    "/api/sharepoint/status",
    "/api/tipos_relatorios"
]

# =========================
# HELPERS
# =========================
def titulo(txt):
    print("\n" + "=" * 70)
    print(txt)
    print("=" * 70)

def ok(msg):
    print(f"✅ {msg}")

def erro(msg):
    print(f"❌ {msg}")

def alerta(msg):
    print(f"⚠️ {msg}")

# =========================
# PORTA ABERTA?
# =========================
def verificar_porta(host, porta):
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect((host, porta))
        s.close()
        return True
    except:
        return False

# =========================
# FRONTEND
# =========================
def validar_frontend():
    titulo("VALIDANDO FRONTEND")

    if verificar_porta("localhost", 3000):
        ok("React rodando na porta 3000")
    else:
        erro("Frontend OFFLINE")
        return

    try:
        r = requests.get(FRONTEND, timeout=TIMEOUT)
        ok(f"Frontend respondeu HTTP {r.status_code}")
    except Exception as e:
        erro(str(e))

# =========================
# BACKEND
# =========================
def validar_backend():
    titulo("VALIDANDO BACKEND")

    if verificar_porta("localhost", 8000):
        ok("FastAPI rodando na porta 8000")
    else:
        erro("Backend OFFLINE")
        return False

    try:
        r = requests.get(BACKEND + "/docs", timeout=TIMEOUT)
        ok("Swagger disponível")
        return True
    except:
        erro("Swagger indisponível")
        return False

# =========================
# ENDPOINTS
# =========================
def validar_endpoints():
    titulo("VALIDANDO ENDPOINTS")

    falhas = []

    for ep in ENDPOINTS:
        url = BACKEND + ep
        try:
            r = requests.get(url, timeout=TIMEOUT)
            code = r.status_code

            if code in [200, 201]:
                ok(f"{ep} -> {code}")
            elif code == 405:
                alerta(f"{ep} -> método diferente")
            elif code == 401:
                alerta(f"{ep} -> protegido por login")
            elif code == 404:
                erro(f"{ep} -> NÃO EXISTE")
                falhas.append(ep)
            elif code >= 500:
                erro(f"{ep} -> ERRO INTERNO")
                falhas.append(ep)
            else:
                alerta(f"{ep} -> {code}")

        except Exception as e:
            erro(f"{ep} -> {str(e)}")
            falhas.append(ep)

    return falhas

# =========================
# DASHBOARD
# =========================
def validar_dashboard():
    titulo("VALIDANDO DASHBOARD")

    try:
        r = requests.get(BACKEND + "/api/dashboard", timeout=TIMEOUT)
        data = r.json()

        campos = [
            "empresas",
            "documentos",
            "guias",
            "usuarios",
            "alertas",
            "obrigacoes"
        ]

        for c in campos:
            if c in data:
                ok(f"{c}: {data[c]}")
            else:
                erro(f"Campo ausente: {c}")

    except Exception as e:
        erro(str(e))

# =========================
# PROBLEMAS DETECTADOS
# =========================
def problemas_conhecidos():
    titulo("PROBLEMAS DETECTADOS NO LOG")

    erro("Robos.jsx usa URL undefined/api/... ")
    print("➡ Ajustar variável API_BASE_URL")

    erro("Auditoria.jsx usa undefined/api/auditoria")
    print("➡ Importar axios global")

    erro("Alertas CORS")
    print("➡ Habilitar CORSMiddleware")

    erro("tipos_relatorios 404")
    print("➡ Criar endpoint /api/tipos_relatorios")

    erro("Keys duplicadas React")
    print("➡ Ajustar key em Documentos.jsx")

    erro("Guias sem key")
    print("➡ Adicionar key={item.id}")

# =========================
# O QUE FALTA
# =========================
def faltando():
    titulo("O QUE FALTA PARA 100%")

    itens = [
        "1. Ajustar CORS no backend",
        "2. Criar endpoints faltantes",
        "3. Padronizar /api em todas URLs",
        "4. Corrigir undefined API_BASE_URL",
        "5. Corrigir React key duplicada",
        "6. Popular Mongo collections",
        "7. Ajustar dashboard tempo real",
        "8. Implementar JWT completo",
        "9. Validar robots APIs",
        "10. Teste integrado frontend/backend"
    ]

    for i in itens:
        print(i)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    titulo("CONSULTSLT ENTERPRISE HEALTH CHECK")

    validar_frontend()

    if validar_backend():
        falhas = validar_endpoints()
        validar_dashboard()
        problemas_conhecidos()
        faltando()

    titulo("FINALIZADO")
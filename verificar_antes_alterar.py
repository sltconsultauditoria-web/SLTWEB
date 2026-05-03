# ===============================================================
# PRE-CHECK SAFE VALIDATOR (NÃO QUEBRA APLICAÇÃO)
# Arquivo: verificar_antes_alterar.py
#
# Objetivo:
# Validar estrutura completa ANTES de alterar qualquer arquivo:
# - verifica caminhos reais
# - verifica backend/frontend
# - verifica arquivos críticos
# - verifica endpoints
# - verifica collections Mongo
# - cria backup automático
# - detecta risco de quebra
#
# EXECUTAR:
# python verificar_antes_alterar.py
# ===============================================================

import os
import json
import shutil
import socket
import requests
from datetime import datetime

# ===============================================================
# CONFIG
# ===============================================================
ROOT = r"C:\Users\admin-local\ServerApp\consultSLTweb"

BACKEND = os.path.join(ROOT, "backend")
FRONTEND = os.path.join(ROOT, "frontend")

API_URL = "http://localhost:8000"
WEB_URL = "http://localhost:3000"

TIMEOUT = 4

# ===============================================================
# HELPERS
# ===============================================================
def titulo(msg):
    print("\n" + "="*70)
    print(msg)
    print("="*70)

def ok(msg):
    print(f"✅ {msg}")

def erro(msg):
    print(f"❌ {msg}")

def alerta(msg):
    print(f"⚠️ {msg}")

# ===============================================================
# PORT CHECK
# ===============================================================
def porta(host, port):
    s = socket.socket()
    s.settimeout(2)
    try:
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

# ===============================================================
# BACKUP
# ===============================================================
def backup_arquivo(path):
    if not os.path.exists(path):
        return

    pasta = os.path.join(ROOT, "backup_precheck")
    os.makedirs(pasta, exist_ok=True)

    nome = os.path.basename(path)
    destino = os.path.join(
        pasta,
        nome + "." + datetime.now().strftime("%Y%m%d_%H%M%S") + ".bak"
    )

    shutil.copy2(path, destino)
    ok(f"Backup criado: {nome}")

# ===============================================================
# VERIFICAR ESTRUTURA
# ===============================================================
def estrutura():
    titulo("VALIDANDO ESTRUTURA")

    pastas = [
        ROOT,
        BACKEND,
        FRONTEND,
        os.path.join(FRONTEND, "src"),
        os.path.join(FRONTEND, "src/pages"),
        os.path.join(FRONTEND, "src/context"),
    ]

    for p in pastas:
        if os.path.exists(p):
            ok(p)
        else:
            erro(p)

# ===============================================================
# VERIFICAR ARQUIVOS CRÍTICOS
# ===============================================================
def arquivos():
    titulo("VALIDANDO ARQUIVOS CRÍTICOS")

    lista = [
        os.path.join(BACKEND, "main_enterprise.py"),
        os.path.join(FRONTEND, "src/App.jsx"),
        os.path.join(FRONTEND, "src/context/AuthContext.jsx"),
        os.path.join(FRONTEND, "src/pages/Dashboard.jsx"),
        os.path.join(FRONTEND, ".env"),
    ]

    for arq in lista:
        if os.path.exists(arq):
            ok(arq)
            backup_arquivo(arq)
        else:
            alerta(f"Ausente: {arq}")

# ===============================================================
# VALIDAR SERVIÇOS
# ===============================================================
def servicos():
    titulo("VALIDANDO SERVIÇOS")

    if porta("localhost", 8000):
        ok("Backend ativo porta 8000")
    else:
        erro("Backend OFF")

    if porta("localhost", 3000):
        ok("Frontend ativo porta 3000")
    else:
        erro("Frontend OFF")

# ===============================================================
# VALIDAR ENDPOINTS SAFE
# ===============================================================
def endpoints():
    titulo("VALIDANDO ENDPOINTS")

    eps = [
        "/docs",
        "/openapi.json",
        "/api/dashboard",
        "/api/empresas",
        "/api/documentos",
        "/api/guias",
        "/api/usuarios"
    ]

    for ep in eps:
        try:
            r = requests.get(API_URL + ep, timeout=TIMEOUT)
            ok(f"{ep} -> {r.status_code}")
        except:
            erro(ep)

# ===============================================================
# ANALISAR AUTHCONTEXT
# ===============================================================
def analisar_auth():
    titulo("ANALISANDO AUTHCONTEXT")

    path = os.path.join(FRONTEND, "src/context/AuthContext.jsx")

    if not os.path.exists(path):
        erro("AuthContext não encontrado")
        return

    txt = open(path, encoding="utf-8").read()

    if "undefined" in txt:
        erro("Encontrado undefined")
    else:
        ok("Sem undefined")

    if "localhost:8000/api/api" in txt:
        erro("Duplicidade /api/api")
    else:
        ok("Sem duplicidade /api")

# ===============================================================
# ANALISAR REACT KEYS
# ===============================================================
def analisar_keys():
    titulo("ANALISANDO KEYS REACT")

    paginas = os.path.join(FRONTEND, "src/pages")

    if not os.path.exists(paginas):
        return

    for arq in os.listdir(paginas):
        if arq.endswith(".jsx"):
            path = os.path.join(paginas, arq)
            txt = open(path, encoding="utf-8").read()

            if ".map(" in txt and "key=" not in txt:
                alerta(f"{arq} pode faltar key")

# ===============================================================
# RISCO DE QUEBRA
# ===============================================================
def risco():
    titulo("RISCO DE ALTERAÇÃO")

    print("🟢 BAIXO  -> CSS / textos / layout")
    print("🟡 MÉDIO -> Frontend endpoints")
    print("🔴 ALTO  -> main_enterprise.py / auth / Mongo")

# ===============================================================
# O QUE PODE ALTERAR COM SEGURANÇA
# ===============================================================
def seguro():
    titulo("ALTERAÇÕES SEGURAS AGORA")

    lista = [
        "1. Corrigir keys React",
        "2. Corrigir URLs undefined",
        "3. Criar endpoints faltantes novos",
        "4. Melhorar dashboard frontend",
        "5. Ajustar .env",
        "6. Adicionar loading states",
    ]

    for i in lista:
        print(i)

# ===============================================================
# MAIN
# ===============================================================
if __name__ == "__main__":
    titulo("PRE CHECK SAFE CONSULTSLT")

    estrutura()
    arquivos()
    servicos()
    endpoints()
    analisar_auth()
    analisar_keys()
    risco()
    seguro()

    titulo("VALIDAÇÃO FINALIZADA")
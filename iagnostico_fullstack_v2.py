import requests
import os
import json

BASE_URL = "http://localhost:8000"
FRONT_ENV = "./frontend/.env"

print("=" * 60)
print("DIAGNOSTICO FULLSTACK SLTWEB - VERSAO AVANCADA")
print("=" * 60)


def check(title):
    print(f"\n🔎 {title}")


# =========================
# 1. BACKEND HEALTH (VARIAS ROTAS)
# =========================
check("1. BACKEND HEALTH")

health_urls = [
    "/api/health",
    "/api/health/health/",
    "/api/health/"
]

for url in health_urls:
    try:
        r = requests.get(BASE_URL + url)
        print(f"{url} → {r.status_code}")
    except:
        print(f"{url} → ERRO")


# =========================
# 2. TESTE API REAL
# =========================
check("2. TESTE API EMPRESAS")

try:
    r = requests.get(f"{BASE_URL}/api/empresas/")
    print("Status:", r.status_code)

    if r.status_code == 200:
        data = r.json()
        print("Registros:", len(data))
    else:
        print("Erro ao acessar empresas")

except Exception as e:
    print("Erro:", e)


# =========================
# 3. TESTE LOGIN
# =========================
check("3. TESTE LOGIN")

try:
    payload = {"username": "admin", "password": "admin"}
    r = requests.post(f"{BASE_URL}/api/login", json=payload)

    print("Status:", r.status_code)

    if r.status_code == 200:
        print("Login OK:", r.json())
    else:
        print("❌ LOGIN NÃO EXISTE ou QUEBRADO")

except Exception as e:
    print("Erro login:", e)


# =========================
# 4. TESTE CORS (CRÍTICO)
# =========================
check("4. TESTE CORS")

try:
    headers = {
        "Origin": "http://localhost:3000"
    }

    r = requests.get(f"{BASE_URL}/api/empresas/", headers=headers)

    if "access-control-allow-origin" in r.headers:
        print("✅ CORS OK")
    else:
        print("❌ CORS NÃO CONFIGURADO (frontend vai quebrar)")

except Exception as e:
    print("Erro CORS:", e)


# =========================
# 5. VALIDAR .ENV
# =========================
check("5. VALIDANDO .ENV")

if os.path.exists(FRONT_ENV):
    with open(FRONT_ENV) as f:
        env = f.read()

    print(env)

    if "localhost:3000" in env:
        print("❌ ERRO GRAVE: API apontando para FRONTEND")

    if "https://" in env:
        print("⚠️ POSSÍVEL ERRO: HTTPS com backend HTTP")

    if "localhost:8000" in env:
        print("✅ API LOCAL OK")

else:
    print("❌ .env NÃO ENCONTRADO")


# =========================
# 6. TESTE BANCO (CRUD REAL)
# =========================
check("6. TESTE BANCO (CRUD)")

try:
    novo = {"nome": "Teste Diagnostico"}

    r = requests.post(f"{BASE_URL}/api/empresas/", json=novo)

    print("POST:", r.status_code)

    if r.status_code in [200, 201]:
        data = r.json()
        item_id = data.get("id")

        print("Criado ID:", item_id)

        # GET
        r2 = requests.get(f"{BASE_URL}/api/empresas/{item_id}")
        print("GET:", r2.status_code)

        # DELETE (limpeza)
        r3 = requests.delete(f"{BASE_URL}/api/empresas/{item_id}")
        print("DELETE:", r3.status_code)

    else:
        print("❌ ERRO INSERT (banco ou schema)")

except Exception as e:
    print("Erro banco:", e)


# =========================
# 7. TESTE PORTA FRONTEND
# =========================
check("7. TESTE FRONTEND")

try:
    r = requests.get("http://localhost:3000")
    print("Frontend:", r.status_code)
except:
    print("❌ Frontend não respondeu")


# =========================
# 8. DETECTAR PROBLEMA REAL
# =========================
check("8. DIAGNOSTICO FINAL")

print("""
Se aparecer:

❌ LOGIN NÃO EXISTE → precisa criar endpoint /api/login
❌ CORS NÃO CONFIGURADO → backend bloqueia frontend
❌ API apontando localhost:3000 → frontend nunca vai funcionar
❌ INSERT falhou → problema no banco (consultslt_db)
❌ Frontend não respondeu → npm start não está ativo

👉 CAUSA MAIS PROVÁVEL NO SEU CASO:
- API URL errada no .env
- Falta de autenticação
- CORS não configurado
""")

print("=" * 60)
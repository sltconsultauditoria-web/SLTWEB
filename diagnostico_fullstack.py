import requests
import os
import json

BASE_URL = "http://localhost:8000"
FRONT_ENV = "./frontend/.env"

print("=" * 50)
print("DIAGNOSTICO FULLSTACK SLTWEB")
print("=" * 50)


# =========================
# 1. BACKEND HEALTH
# =========================
print("\n[1] Testando backend...")

try:
    r = requests.get(f"{BASE_URL}/api/health")
    print("Status:", r.status_code)

    if r.status_code == 200:
        print("Backend OK")
    else:
        print("Backend respondeu com erro")

except Exception as e:
    print("ERRO backend:", e)


# =========================
# 2. TESTAR ENDPOINT REAL
# =========================
print("\n[2] Testando API empresas...")

try:
    r = requests.get(f"{BASE_URL}/api/empresas/")
    print("Status:", r.status_code)

    if r.status_code == 200:
        print("API funcionando")
        print("Qtd registros:", len(r.json()))
    else:
        print("Erro ao buscar dados")

except Exception as e:
    print("Erro:", e)


# =========================
# 3. TESTE LOGIN
# =========================
print("\n[3] Testando LOGIN (simulado)...")

try:
    payload = {
        "username": "admin",
        "password": "admin"
    }

    r = requests.post(f"{BASE_URL}/api/login", json=payload)

    if r.status_code == 200:
        print("Login OK")
        print(r.json())
    else:
        print("LOGIN NÃO IMPLEMENTADO ou falhando:", r.status_code)

except Exception as e:
    print("Erro login:", e)


# =========================
# 4. VALIDAR .ENV FRONTEND
# =========================
print("\n[4] Validando .env frontend...")

if os.path.exists(FRONT_ENV):
    with open(FRONT_ENV) as f:
        env = f.read()

    if "localhost:3000" in env:
        print("❌ ERRO: API apontando para frontend")

    if "localhost:8000" in env:
        print("✅ API correta")

else:
    print("❌ .env não encontrado")


# =========================
# 5. TESTAR BANCO VIA API
# =========================
print("\n[5] Testando persistência (CRUD)...")

try:
    novo = {"nome": "Teste Script"}

    r = requests.post(f"{BASE_URL}/api/empresas/", json=novo)

    if r.status_code in [200, 201]:
        print("INSERT OK")

        data = r.json()
        item_id = data.get("id")

        # GET
        r2 = requests.get(f"{BASE_URL}/api/empresas/{item_id}")
        print("GET OK:", r2.status_code)

    else:
        print("Erro ao inserir:", r.status_code)

except Exception as e:
    print("Erro banco:", e)


# =========================
# 6. CONCLUSÃO
# =========================
print("\n" + "=" * 50)
print("RESUMO:")
print("- Se login falhou → precisa implementar autenticação")
print("- Se empresas falhou → problema banco ou ORM")
print("- Se .env errado → frontend nunca vai funcionar")
print("=" * 50)
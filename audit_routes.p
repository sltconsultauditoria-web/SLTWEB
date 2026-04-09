import requests

BASE_URL = "http://localhost:8000"

# rotas que o frontend espera
EXPECTED_ROUTES = [
    ("POST", "/api/auth/login"),
    ("GET", "/api/auth/me"),
    ("GET", "/api/auth/usuarios"),
]

print("\n=== TESTANDO ROTAS ===\n")

for method, route in EXPECTED_ROUTES:

    url = BASE_URL + route

    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json={})
        else:
            continue

        print(f"{method} {route} -> {response.status_code}")

    except Exception as e:
        print(f"{method} {route} -> ERRO: {e}")


print("\n=== VERIFICAÇÃO FINAL ===\n")

for method, route in EXPECTED_ROUTES:
    url = BASE_URL + route

    try:
        response = requests.get(url)

        if response.status_code == 404:
            print(f"❌ FALTANDO: {route}")
        else:
            print(f"✅ OK: {route}")

    except:
        print(f"⚠️ ERRO AO ACESSAR: {route}")
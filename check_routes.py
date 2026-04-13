import requests

BASE_URL = "http://localhost:3000"

# Rotas que o frontend espera
expected_routes = [
    "/api/empresas",
    "/api/dashboard",
    "/api/documentos",
    "/api/fiscal",
    "/api/ocr",
    "/api/usuarios",
    "/api/obrigacoes"
]

def check_routes():
    for route in expected_routes:
        try:
            r = requests.get(BASE_URL + route)
            if r.status_code == 200:
                print(f"✔ {route} OK")
            else:
                print(f"⚠ {route} retornou {r.status_code}")
        except Exception as e:
            print(f"❌ {route} erro de conexão: {e}")

if __name__ == "__main__":
    check_routes()

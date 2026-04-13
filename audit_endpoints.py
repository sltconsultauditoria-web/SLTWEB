# audit_endpoints.py
import httpx
import re

BASE_URL = "http://localhost:8000"

def extract_routes_from_main(file_path="backend/main_enterprise.py"):
    routes = []
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    # Captura linhas como: app.include_router(guias.router, prefix="/api/guias")
    matches = re.findall(r'prefix="(/api/[a-zA-Z0-9_]+)"', content)
    routes.extend(matches)
    return routes

def audit_routes(routes):
    with httpx.Client(timeout=5.0) as client:
        for route in routes:
            url = f"{BASE_URL}{route}"
            try:
                response = client.get(url)
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if isinstance(data, list):
                            print(f"✅ {route} OK ({len(data)} registros)")
                        else:
                            print(f"✅ {route} OK (resposta JSON)")
                    except Exception:
                        print(f"✅ {route} OK (resposta não é JSON)")
                else:
                    print(f"❌ {route} retornou {response.status_code}")
            except Exception as e:
                print(f"⚠️ Erro ao acessar {route}: {e}")

if __name__ == "__main__":
    routes = extract_routes_from_main()
    print("📌 Rotas encontradas no main_enterprise.py:")
    for r in routes:
        print(" -", r)
    print("\n📊 Testando rotas...\n")
    audit_routes(routes)

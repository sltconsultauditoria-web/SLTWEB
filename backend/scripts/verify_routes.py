import requests

def verify_routes(base_url):
    routes = [
        "/api/alertas",
        "/api/guias",
        "/api/obrigacoes",
        "/api/auth/login",
        "/api/auth/test-password"
    ]

    for route in routes:
        try:
            response = requests.get(f"{base_url}{route}")
            print(f"Route: {route} - Status: {response.status_code}")
        except Exception as e:
            print(f"Route: {route} - Error: {e}")

if __name__ == "__main__":
    base_url = "http://localhost:8000"
    verify_routes(base_url)
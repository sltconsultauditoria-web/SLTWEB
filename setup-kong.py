import requests

BASE_URL = "http://localhost:9001"

print("🚀 Criando serviço consultslt-service...")
resp = requests.post(f"{BASE_URL}/services", data={
    "name": "consultslt-service",
    "url": "http://localhost:8000"
})
print(resp.status_code, resp.text)

print("🚀 Criando rota /api para consultslt-service...")
resp = requests.post(f"{BASE_URL}/services/consultslt-service/routes", data={
    "paths[]": "/api"
})
print(resp.status_code, resp.text)

print("🚀 Ativando plugin CORS...")
resp = requests.post(f"{BASE_URL}/services/consultslt-service/plugins", data={
    "name": "cors",
    "config.origins": "https://sltconsultauditoria-web.github.io",
    "config.methods": "GET,POST,PUT,DELETE,OPTIONS",
    "config.headers": "Authorization,Content-Type",
    "config.credentials": "true"
})
print(resp.status_code, resp.text)

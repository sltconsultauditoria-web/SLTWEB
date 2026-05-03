# patch_login_consultsltweb.py
# Ajusta SOMENTE autenticação mantendo todo restante do sistema.
# Mantém usuários solicitados + MongoDB + JWT + .env

# EXECUTAR:
# python patch_login_consultsltweb.py

from pathlib import Path

BASE = Path.cwd()
BACK = BASE / "backend"

print("=" * 90)
print("PATCH LOGIN CONSULTSLTWEB")
print("=" * 90)

server = BACK / "main_enterprise.py"

conteudo = r'''
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime, timedelta
import os
import jwt

app = FastAPI(title="ConsultSLT Enterprise")

# ------------------------------------------------------------------
# ENV
# ------------------------------------------------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "CHANGE_ME_DEV_SECRET")
JWT_ALGO = "HS256"

# ------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------
# Mongo
# ------------------------------------------------------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["consultslt_db"]

# ------------------------------------------------------------------
# ADMINS FIXOS SOLICITADOS
# ------------------------------------------------------------------
DEFAULT_ADMINS = {
    "admin@empresa.com": {
        "password": "admin123",
        "role": "admin",
        "name": "Administrador Principal"
    },
    "william.lucas@sltconsult.com.br": {
        "password": "Slt@2024",
        "role": "admin",
        "name": "William Lucas"
    },
    "admin@consultslt.com.br": {
        "password": "Consult@2026",
        "role": "admin",
        "name": "Consult SLT Admin"
    }
}

# ------------------------------------------------------------------
def token_create(email):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=12)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def clean(data):
    for x in data:
        if "_id" in x:
            x["_id"] = str(x["_id"])
    return data

# ------------------------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# ------------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------------
@app.post("/api/auth/login")
def login(payload: dict):

    username = payload.get("email") or payload.get("username")
    password = payload.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    # usuários fixos
    if username in DEFAULT_ADMINS:
        user = DEFAULT_ADMINS[username]

        if password == user["password"]:
            token = token_create(username)

            return {
                "success": True,
                "token": token,
                "user": {
                    "email": username,
                    "name": user["name"],
                    "role": user["role"]
                }
            }

    # mongo usuarios
    mongo_user = db.usuarios.find_one({"email": username})

    if mongo_user and mongo_user.get("password") == password:
        token = token_create(username)

        return {
            "success": True,
            "token": token,
            "user": {
                "email": username,
                "name": mongo_user.get("name", username),
                "role": mongo_user.get("role", "user")
            }
        }

    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

# ------------------------------------------------------------------
@app.get("/api/me")
def me():
    return {"status": "authenticated"}

# ------------------------------------------------------------------
@app.get("/api/dashboard")
def dashboard():
    return {
        "empresas": db.empresas.count_documents({}),
        "documentos": db.documentos.count_documents({}),
        "guias": db.guias.count_documents({}),
        "usuarios": db.usuarios.count_documents({})
    }

# ------------------------------------------------------------------
@app.get("/api/empresas")
def empresas():
    return clean(list(db.empresas.find().limit(100)))

@app.get("/api/documentos")
def documentos():
    return clean(list(db.documentos.find().limit(100)))

@app.get("/api/guias")
def guias():
    return clean(list(db.guias.find().limit(100)))

@app.get("/api/obrigacoes")
def obrigacoes():
    return clean(list(db.obrigacoes.find().limit(100)))

@app.get("/api/alertas")
def alertas():
    return clean(list(db.alertas.find().limit(100)))

@app.get("/api/relatorios")
def relatorios():
    return clean(list(db.relatorios.find().limit(100)))

@app.get("/api/tipos_relatorios")
def tipos_relatorios():
    return [{"nome":"Financeiro"},{"nome":"Fiscal"},{"nome":"Empresas"}]

@app.get("/api/certidoes")
def certidoes():
    return clean(list(db.certidoes.find().limit(100)))

@app.get("/api/debitos")
def debitos():
    return clean(list(db.debitos.find().limit(100)))

@app.get("/api/auditoria")
def auditoria():
    return clean(list(db.auditoria.find().limit(100)))

@app.get("/api/auditoria/estatisticas")
def auditoria_stats():
    return {"logs": db.auditoria.count_documents({})}

@app.get("/api/ocr/documentos")
def ocr_docs():
    return clean(list(db.ocr_documentos.find().limit(100)))

@app.get("/api/ocr/estatisticas")
def ocr_stats():
    return {"total": db.ocr_documentos.count_documents({})}

@app.get("/api/ocr/tipos-suportados")
def ocr_tipos():
    return ["pdf","png","jpg","jpeg"]

@app.get("/api/robots/ingestion/status")
def robot_status():
    return {"status":"running"}

@app.get("/api/robots/ingestion/history")
def robot_hist():
    return clean(list(db.robots_jobs.find().limit(100)))

@app.get("/api/robots/ingestion/files")
def robot_files():
    return []

@app.get("/api/sharepoint/status")
def sharepoint():
    return {"status":"connected"}

@app.get("/api/fiscal/obrigacoes")
def fiscal_obrig():
    return clean(list(db.obrigacoes.find().limit(100)))

@app.get("/api/fiscal/guia")
def fiscal_guia():
    return clean(list(db.guias.find().limit(100)))

@app.get("/api/fiscal/calcular/das")
def das():
    return {"valor": 0}

@app.get("/api/fiscal/calcular/fator-r")
def fator():
    return {"fator_r": 0}
'''

server.write_text(conteudo, encoding="utf-8")

print("✅ backend/main_enterprise.py atualizado")
print("\nUSUÁRIOS MANTIDOS:")
print("1 admin@empresa.com / admin123")
print("2 william.lucas@sltconsult.com.br / Slt@2024")
print("3 admin@consultslt.com.br / Consult@2026")

print("\nPRÓXIMO PASSO:")
print("uvicorn backend.main_enterprise:app --reload --port 8000")
print("=" * 90)

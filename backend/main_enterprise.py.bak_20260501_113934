
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from datetime import datetime
import os

app = FastAPI(title="CONSULTSLT ENTERPRISE")

# ======================================================
# CORS
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# MONGO
# ======================================================
MONGO_URL = "mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["consultslt_db"]


# ======================================================
# HELPERS
# ======================================================
def safe_count(nome):
    try:
        return db[nome].count_documents({})
    except:
        return 0


def now():
    return str(datetime.now())


# ======================================================
# HEALTH
# ======================================================
@app.get("/")
def root():
    return {"app": "CONSULTSLT", "status": "online"}


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "mongo": "ok",
        "timestamp": now()
    }


# ======================================================
# AUTH
# ======================================================
@app.post("/api/auth/login")
def login(payload: dict):
    email = payload.get("email", "")
    senha = payload.get("password", "")

    if email and senha:
        return {
            "success": True,
            "token": "jwt-enterprise-token",
            "user": {
                "email": email,
                "nome": "Administrador",
                "role": "admin"
            }
        }

    return {"success": False}


@app.get("/api/me")
def me():
    return {
        "email": "admin@consultslt.com",
        "nome": "Administrador",
        "role": "admin"
    }


# ======================================================
# DASHBOARD
# ======================================================
@app.get("/api/dashboard")
def dashboard():

    empresas = safe_count("empresas")
    documentos = safe_count("documentos")
    guias = safe_count("guias")
    usuarios = safe_count("usuarios")
    alertas = safe_count("alertas")
    obrigacoes = safe_count("obrigacoes")

    return {
        "success": True,
        "empresas": empresas,
        "documentos": documentos,
        "guias": guias,
        "usuarios": usuarios,
        "alertas": alertas,
        "obrigacoes": obrigacoes,
        "usuariosOnline": 2,
        "saudeSistema": "OK",
        "updatedAt": now()
    }


# ======================================================
# CRUDS
# ======================================================
@app.get("/api/empresas")
def empresas():
    return list(db["empresas"].find({}, {"_id": 0}))


@app.get("/api/documentos")
def documentos():
    return list(db["documentos"].find({}, {"_id": 0}))


@app.get("/api/guias")
def guias():
    return list(db["guias"].find({}, {"_id": 0}))


@app.get("/api/usuarios")
def usuarios():
    return list(db["usuarios"].find({}, {"_id": 0}))


@app.get("/api/alertas")
def alertas():
    return list(db["alertas"].find({}, {"_id": 0}))


@app.get("/api/obrigacoes")
def obrigacoes():
    return list(db["obrigacoes"].find({}, {"_id": 0}))


@app.get("/api/auditoria")
def auditoria():
    return list(db["auditorias"].find({}, {"_id": 0}))


@app.get("/api/auditoria/estatisticas")
def auditoria_stats():
    return {
        "total": safe_count("auditorias"),
        "ultima_execucao": now()
    }


# ======================================================
# ROBOTS
# ======================================================
@app.get("/api/robots/ingestion/status")
def robot_status():
    return {
        "status": "running",
        "jobs": safe_count("robots")
    }


@app.get("/api/robots/ingestion/files")
def robot_files():
    return [
        {"arquivo": "empresa1.pdf"},
        {"arquivo": "empresa2.pdf"}
    ]


@app.get("/api/robots/ingestion/history")
def robot_history():
    return [
        {"data": now(), "status": "ok"}
    ]


# ======================================================
# SHAREPOINT
# ======================================================
@app.get("/api/sharepoint/status")
def sharepoint():
    return {
        "status": "connected",
        "sync": True
    }


# ======================================================
# RELATÓRIOS
# ======================================================
@app.get("/api/tipos_relatorios")
def tipos_relatorios():
    return list(db["tipos_relatorios"].find({}, {"_id": 0}))


@app.get("/api/relatorios")
def relatorios():
    return list(db["relatorios"].find({}, {"_id": 0}))

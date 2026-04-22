from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone, timedelta
from jose import jwt
import os
import uuid
import bcrypt
import logging

# --------------------------------------------------
# CONFIGURAÇÃO INICIAL
# --------------------------------------------------
BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consultslt")

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "consultslt")
JWT_SECRET = os.getenv("JWT_SECRET", "consultslt-secret")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]

app = FastAPI(
    title="ConsultSLT API",
    version="1.0.0"
)

api_router = APIRouter(prefix="/api")

# --------------------------------------------------
# MODELS
# --------------------------------------------------
class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None

class UserCreate(BaseModel):
    email: str
    password: str
    name: str
    role: str = "USER"

# --------------------------------------------------
# ADMINS PADRÃO (SEED)
# --------------------------------------------------
DEFAULT_ADMINS = [
    {
        "email": "admin@empresa.com",
        "password": "admin123",
        "name": "Administrador",
        "role": "ADMIN",
    },
    {
        "email": "william.lucas@sltconsult.com.br",
        "password": "Slt@2024",
        "name": "William Lucas",
        "role": "ADMIN",
    },
    {
        "email": "admin@consultslt.com.br",
        "password": "Consult@2026",
        "name": "Admin SLT",
        "role": "ADMIN",
    },
]

# --------------------------------------------------
# FUNÇÕES AUXILIARES
# --------------------------------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())

def generate_token(user: dict) -> str:
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "exp": datetime.now(timezone.utc) + timedelta(days=1)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# --------------------------------------------------
# SEED DE ADMINS (STARTUP)
# --------------------------------------------------
async def ensure_default_admins():
    for admin in DEFAULT_ADMINS:
        exists = await db.users.find_one({"email": admin["email"]})
        if not exists:
            await db.users.insert_one({
                "id": str(uuid.uuid4()),
                "email": admin["email"],
                "password_hash": hash_password(admin["password"]),
                "name": admin["name"],
                "role": admin["role"],
                "active": True,
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
            logger.info(f"✓ Admin criado: {admin['email']}")

# --------------------------------------------------
# ROTAS
# --------------------------------------------------
@api_router.get("/")
async def root():
    return {"status": "ConsultSLT API Online"}

@api_router.post("/auth/login", response_model=LoginResponse)
async def login(data: LoginRequest):
    user = await db.users.find_one({"email": data.email})
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # Compatibilidade com dados antigos e novos
    password_hash = user.get("password_hash") or user.get("password")

    if not password_hash or not verify_password(data.password, password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = generate_token(user)

    return LoginResponse(
        success=True,
        message="Login realizado com sucesso",
        token=token,
        user={
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
    )

@api_router.post("/auth/register", response_model=LoginResponse)
async def register(data: UserCreate):
    exists = await db.users.find_one({"email": data.email})
    if exists:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    user = {
        "id": str(uuid.uuid4()),
        "email": data.email,
        "password_hash": hash_password(data.password),
        "name": data.name,
        "role": data.role,
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    await db.users.insert_one(user)
    token = generate_token(user)

    return LoginResponse(
        success=True,
        message="Usuário criado com sucesso",
        token=token,
        user={
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
    )

# --------------------------------------------------
# REGISTRO
# --------------------------------------------------
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# STARTUP / SHUTDOWN
# --------------------------------------------------
@app.on_event("startup")
async def startup():
    logger.info("🚀 Iniciando ConsultSLT API")
    await ensure_default_admins()
    logger.info("✅ Sistema pronto")

@app.on_event("shutdown")
async def shutdown():
    client.close()
    logger.info("🛑 MongoDB desconectado")

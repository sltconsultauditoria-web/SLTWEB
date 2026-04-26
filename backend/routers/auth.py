from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
import jwt
import os

# ==========================================================
# ROUTER
# ==========================================================

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

# ==========================================================
# CONFIG
# ==========================================================

JWT_SECRET = os.getenv(
    "JWT_SECRET",
    "sltdctfweb-secret-key-2024"
)

JWT_ALGORITHM = "HS256"

# ==========================================================
# DEFAULT ADMINS
# ==========================================================

DEFAULT_ADMINS = {
    "admin@empresa.com": "admin123",
    "william.lucas@sltconsult.com.br": "Slt@2024",
    "admin@consultslt.com.br": "Consult@2026",
}

# ==========================================================
# MODELS
# ==========================================================

class LoginRequest(BaseModel):
    email: str
    password: str


# ==========================================================
# TOKEN
# ==========================================================

def generate_token(email: str):
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }

    return jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )


# ==========================================================
# LOGIN
# ==========================================================

@router.post("/login")
async def login(data: LoginRequest):

    email = data.email.lower().strip()
    password = data.password.strip()

    if email not in DEFAULT_ADMINS:
        raise HTTPException(
            status_code=401,
            detail="Usuário não autorizado"
        )

    if DEFAULT_ADMINS[email] != password:
        raise HTTPException(
            status_code=401,
            detail="Senha inválida"
        )

    token = generate_token(email)

    return {
        "success": True,
        "token": token,
        "token_type": "bearer",
        "user": {
            "email": email,
            "role": "admin"
        }
    }


# ==========================================================
# HEALTH
# ==========================================================

@router.get("/health")
async def auth_health():
    return {
        "status": "online",
        "module": "auth"
    }
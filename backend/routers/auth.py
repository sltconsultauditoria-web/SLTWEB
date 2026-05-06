from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr

from backend.core.database import get_db
from backend.core.security import (
    create_access_token,
    verify_password,
    get_current_user,   # se existir no seu security.py
)

# =====================================================
# Router
# main_enterprise.py usa prefix="/api"
# Resultado final:
# /api/auth/login
# /api/auth/me
# /api/auth/health
# =====================================================
router = APIRouter(prefix="/auth", tags=["Auth"])

# =====================================================
# Mongo
# =====================================================
db = get_db()

# =====================================================
# Admins default seguros
# =====================================================
DEFAULT_ADMINS = {
    "admin@empresa.com": {
        "password": "admin123",
        "name": "Administrador",
        "role": "admin",
    },
    "admin@consultslt.com.br": {
        "password": "Consult@2026",
        "name": "Administrador",
        "role": "admin",
    },
    "william.lucas@sltconsult.com.br": {
        "password": "Slt@2024",
        "name": "William Lucas",
        "role": "admin",
    },
}

# =====================================================
# Schemas
# =====================================================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# =====================================================
# Helpers
# =====================================================
def serialize_user(user: dict) -> dict:
    return {
        "id": str(user.get("_id", "")),
        "email": user.get("email", ""),
        "name": user.get("nome")
        or user.get("name")
        or "Usuário",
        "role": user.get("role")
        or user.get("perfil")
        or "user",
        "ativo": user.get("ativo", True),
    }


async def find_user(email: str) -> Optional[dict]:
    """
    Procura usuário nas coleções reais
    """
    for collection in ["usuarios", "users"]:
        try:
            user = await db[collection].find_one({"email": email})
            if user:
                return user
        except:
            pass
    return None


# =====================================================
# LOGIN
# =====================================================
@router.post("/login")
async def login(payload: LoginRequest):
    email = payload.email.strip().lower()
    password = payload.password.strip()

    # -------------------------------------------------
    # MongoDB
    # -------------------------------------------------
    user = await find_user(email)

    if user:
        stored_password = (
            user.get("hashed_password")
            or user.get("senha_hash")
            or user.get("password_hash")
            or user.get("password")
            or user.get("senha")
        )

        valid = False

        if stored_password:
            try:
                valid = verify_password(password, stored_password)
            except:
                valid = password == stored_password

        if not valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )

        user_data = serialize_user(user)

    # -------------------------------------------------
    # Admin padrão
    # -------------------------------------------------
    elif email in DEFAULT_ADMINS:
        admin = DEFAULT_ADMINS[email]

        if password != admin["password"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )

        user_data = {
            "id": "admin",
            "email": email,
            "name": admin["name"],
            "role": admin["role"],
            "ativo": True,
        }

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado",
        )

    # -------------------------------------------------
    # JWT
    # =================================================
    token = create_access_token(
        data={
            "sub": user_data["email"],
            "email": user_data["email"],
            "role": user_data["role"],
            "name": user_data["name"],
        },
        expires_delta=timedelta(hours=24),
    )

    return {
        "success": True,
        "message": "Login realizado com sucesso",
        "data": {
            "token": token,
            "access_token": token,
            "token_type": "bearer",
            "user": user_data,
        },
        "token": token,
        "access_token": token,
        "token_type": "bearer",
        "user": user_data,
    }


# =====================================================
# USUÁRIO LOGADO
# =====================================================
@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    return {
        "success": True,
        "data": current_user,
    }


# =====================================================
# HEALTH
# =====================================================
@router.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "auth",
        "database": "consultslt_db",
    }

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from jose import jwt
from passlib.context import CryptContext

from backend.core.database import get_database

# ==========================================================
# CONFIG
# ==========================================================

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

SECRET_KEY = "sltdctfweb-secret-key-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==========================================================
# DEFAULT ADMINS
# ==========================================================

DEFAULT_ADMINS = [
    {
        "email": "admin@empresa.com",
        "password": "admin123",
        "name": "Administrador",
        "role": "admin"
    },
    {
        "email": "william.lucas@sltconsult.com.br",
        "password": "Slt@2024",
        "name": "William Lucas",
        "role": "admin"
    },
    {
        "email": "admin@consultslt.com.br",
        "password": "Consult@2026",
        "name": "Admin Consult SLT",
        "role": "admin"
    }
]


# ==========================================================
# SCHEMAS
# ==========================================================

class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict


# ==========================================================
# HELPERS
# ==========================================================

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(hours=8)
    )

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(email: str, password: str, db=None):

    # 1 - verifica admins padrão
    for admin in DEFAULT_ADMINS:
        if (
            admin["email"].lower() == email.lower()
            and admin["password"] == password
        ):
            return admin

    # 2 - verifica MongoDB (opcional)
    if db:
        user = await db.users.find_one({"email": email})

        if user:
            db_password = user.get("password")

            if db_password == password:
                return {
                    "email": user["email"],
                    "name": user.get("name", user["email"]),
                    "role": user.get("role", "user")
                }

            try:
                if pwd_context.verify(password, db_password):
                    return {
                        "email": user["email"],
                        "name": user.get("name", user["email"]),
                        "role": user.get("role", "user")
                    }
            except Exception:
                pass

    return None


# ==========================================================
# ROUTES
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login do sistema"
)
async def login(
    payload: LoginRequest,
    db=Depends(get_database)
):

    user = await authenticate_user(
        payload.email,
        payload.password,
        db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )

    token = create_access_token(
        {
            "sub": user["email"],
            "role": user["role"],
            "name": user["name"]
        },
        timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "email": user["email"],
            "name": user["name"],
            "role": user["role"]
        }
    }


@router.get("/me")
async def me():
    return {"message": "Use o token JWT no frontend"}


@router.get("/health")
async def auth_health():
    return {"status": "ok", "service": "auth"}
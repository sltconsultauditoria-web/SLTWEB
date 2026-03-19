from datetime import datetime, timedelta
from typing import Optional
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorDatabase
from jose import jwt, JWTError
from passlib.context import CryptContext
from bson import ObjectId

# --- CORREÇÃO FINAL APLICADA AQUI ---
# O caminho da importação foi ajustado para o que o seu projeto espera,
# conforme indicado pelo último log de erro.
from backend.core.database import get_db 
# ------------------------------------

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

SECRET_KEY = os.getenv("JWT_SECRET", "consult-slt-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 8

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

# O prefixo foi removido corretamente. O main_enterprise.py já cuida disso.
router = APIRouter(
    tags=["Autenticação"]
)


# ==========================================================
# MODELS (SCHEMAS) Pydantic
# ==========================================================

class LoginRequest(BaseModel):
    email: str
    password: str

class UserData(BaseModel):
    id: str
    nome: Optional[str] = None
    email: str
    role: Optional[str] = None
    perfil: Optional[str] = None

class TokenData(BaseModel):
    token: str
    user: UserData

class TokenResponse(BaseModel):
    success: bool
    message: str
    data: TokenData


# ==========================================================
# FUNÇÕES DE UTILIDADE
# ==========================================================

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde ao hash salvo."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um novo token de acesso JWT."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==========================================================
# ENDPOINT DE LOGIN
# ==========================================================

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Autentica um usuário e retorna um token de acesso.
    """
    user = await db.usuarios.find_one({"email": {"$regex": f"^{request.email}$", "$options": "i"}})
    if not user or not verify_password(request.password, user.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas. Verifique o email e a senha.",
        )
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Este usuário está inativo e não pode fazer login.",
        )
    token_data = {"sub": str(user["_id"]), "email": user["email"], "role": user.get("role", "user")}
    access_token = create_access_token(token_data)
    await db.usuarios.update_one({"_id": user["_id"]}, {"$set": {"last_login": datetime.utcnow()}})
    return {
        "success": True,
        "message": "Login realizado com sucesso",
        "data": {
            "token": access_token,
            "user": {
                "id": str(user["_id"]),
                "nome": user.get("nome"),
                "email": user.get("email"),
                "role": user.get("role"),
                "perfil": user.get("perfil"),
            }
        }
    }


# ==========================================================
# FUNÇÃO PARA OBTER USUÁRIO ATUAL (PROTEÇÃO DE ROTAS)
# ==========================================================

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncIOMotorDatabase = Depends(get_db)):
    """
    Decodifica o token JWT para obter o usuário atual.
    Usado como uma dependência em rotas protegidas.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    try:
        user = await db.usuarios.find_one({"_id": ObjectId(user_id)})
    except Exception:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user


# ==========================================================
# ENDPOINT PARA VERIFICAR O TOKEN E OBTER DADOS DO USUÁRIO
# ==========================================================

@router.get("/me", response_model=UserData)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    Retorna os dados do usuário autenticado.
    Rota protegida que valida o token.
    """
    return {
        "id": str(current_user["_id"]),
        "nome": current_user.get("nome"),
        "email": current_user.get("email"),
        "role": current_user.get("role"),
        "perfil": current_user.get("perfil"),
    }

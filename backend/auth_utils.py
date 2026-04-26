"""
Utilitários de autenticação - ConsultSLT
Funções de hash de senha, criação e verificação de JWT
"""
import os
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional

import bcrypt
from jose import JWTError, jwt
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

# ============================================================
# Configurações JWT
# ============================================================
JWT_SECRET = os.getenv("JWT_SECRET", "consultslt-secret-2026")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "1440"))


# ============================================================
# Funções de senha
# ============================================================
def hash_password(password: str) -> str:
    """Gera hash bcrypt de uma senha."""
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica se uma senha corresponde ao hash."""
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


# ============================================================
# Funções de token JWT
# ============================================================
def create_access_token(user_id: str, email: str, role: str = "user") -> str:
    """Cria um token JWT de acesso."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=JWT_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[Dict]:
    """Decodifica e valida um token JWT."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        return None


# ============================================================
# Lógica de login com MongoDB
# ============================================================
async def verify_user_credentials(
    db: AsyncIOMotorDatabase,
    email: str,
    password: str
) -> Optional[Dict]:
    """
    Verifica credenciais do usuário no MongoDB.
    Retorna dict com dados do usuário e token, ou None.
    """
    try:
        user = await db["usuarios"].find_one({"email": email})

        if not user:
            logger.warning(f"Usuário não encontrado: {email}")
            return None

        # Suporta tanto 'senha_hash' quanto 'hashed_password'
        hashed_password = user.get("senha_hash") or user.get("hashed_password")

        if not hashed_password:
            logger.error(f"Usuário sem hash de senha: {email}")
            return None

        if not verify_password(password, hashed_password):
            logger.warning(f"Senha incorreta para: {email}")
            return None

        if not user.get("ativo", True):
            logger.warning(f"Usuário inativo: {email}")
            return None

        user_id = str(user.get("_id", user.get("id", "")))
        role = user.get("perfil", user.get("role", "user"))

        token = create_access_token(user_id, email, role)

        return {
            "id": user_id,
            "nome": user.get("nome", ""),
            "email": email,
            "role": role,
            "ativo": user.get("ativo", True),
            "token": token,
        }

    except Exception as e:
        logger.error(f"Erro ao verificar credenciais: {e}")
        return None

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from typing import Dict, Any, Optional

# ==============================
# CONFIGURAÇÃO SEGURA
# ==============================
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60        # 1h
REFRESH_TOKEN_EXPIRE_DAYS = 7           # 7 dias

# ==============================
# PASSWORD HASHING
# ==============================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ==============================
# JWT CORE
# ==============================
def _create_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """
    Cria token JWT base sem mutar input
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc)
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ==============================
# ACCESS TOKEN
# ==============================
def create_access_token(subject: str, extra: Optional[Dict[str, Any]] = None) -> str:
    """
    Token de acesso curto (login)
    subject = user_id ou email
    """
    data = {
        "sub": subject,
        "type": "access"
    }

    if extra:
        data.update(extra)

    return _create_token(
        data,
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


# ==============================
# REFRESH TOKEN
# ==============================
def create_refresh_token(subject: str) -> str:
    """
    Token longo para renovar access token
    """
    data = {
        "sub": subject,
        "type": "refresh"
    }

    return _create_token(
        data,
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


# ==============================
# DECODIFICAR TOKEN
# ==============================
def decode_token(token: str) -> Dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        raise Exception(f"Token inválido: {str(e)}")


# ==============================
# VALIDAR TIPO DE TOKEN
# ==============================
def is_refresh_token(payload: Dict[str, Any]) -> bool:
    return payload.get("type") == "refresh"


def is_access_token(payload: Dict[str, Any]) -> bool:
    return payload.get("type") == "access"
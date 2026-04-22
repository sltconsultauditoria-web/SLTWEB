from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import logging

# Configuração do logger
logger = logging.getLogger("auth")
logger.setLevel(logging.DEBUG)

# Configurações
SECRET_KEY = "sua_chave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuração do bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]
usuarios_collection = db["usuarios"]

# Inicializar o router
router = APIRouter()

# Modelo de requisição
class LoginRequest(BaseModel):
    email: str
    password: str

# Função para verificar senha
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Função para criar token de acesso
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Endpoint de login
@router.post("/auth/login")
async def login(data: LoginRequest):
    logger.info(f"Tentativa de login para o email: {data.email}")
    user = usuarios_collection.find_one({"email": data.email})

    if not user:
        logger.warning(f"Usuário não encontrado: {data.email}")
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    logger.info(f"Usuário encontrado: {user['email']}")

    try:
        if not verify_password(data.password, user["hashed_password"]):
            logger.warning(f"Senha incorreta para o email: {data.email}")
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no servidor")

    token = create_access_token({"sub": user["email"]})
    logger.info(f"Login bem-sucedido para o email: {data.email}")

    return {
        "success": True,
        "message": "Login realizado com sucesso",
        "data": {
            "token": token,
            "user": {
                "email": user["email"],
                "nome": user["nome"],
                "role": user["role"],
                "permissoes": user["permissoes"]
            }
        }
    }

# Endpoint de teste para verificar senha
@router.get("/test-password")
async def test_password():
    from passlib.context import CryptContext

    # Configuração do bcrypt
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Dados de teste
    email = "william.lucas@sltconsult.com.br"
    password = "Slt@2024"

    # Simulação de busca no banco de dados
    user = {
        "email": "william.lucas@sltconsult.com.br",
        "hashed_password": "$2b$12$jtZ8a5Zh9P714VIKTJATlO3Csa6kwCAb.Z2pHmyN7MxdzpX8SWLE2"
    }

    if not user:
        return {"success": False, "message": "Usuário não encontrado"}

    # Verificar senha
    is_valid = pwd_context.verify(password, user["hashed_password"])

    return {
        "success": is_valid,
        "message": "Senha válida" if is_valid else "Senha inválida"
    }
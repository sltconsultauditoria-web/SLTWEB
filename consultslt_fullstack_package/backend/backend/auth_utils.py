import os
import jwt
import bcrypt
from datetime import datetime, timezone, timedelta
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase # Import para type hinting
from typing import Dict, Optional

# ==========================================================
# ⚙️ CONFIGURAÇÕES DO TOKEN
# ==========================================================
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

# ==========================================================
# 🔐 FUNÇÕES DE SENHA
# ==========================================================

def hash_password(password: str) -> str:
    """
    Gera o hash de uma senha usando bcrypt.
    """
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se uma senha corresponde ao seu hash.
    Retorna False em caso de erro para evitar exceções.
    """
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except (ValueError, TypeError):
        # Se o hash for inválido ou ocorrer outro erro, a senha não corresponde.
        return False

# ==========================================================
# 🔑 FUNÇÕES DE TOKEN
# ==========================================================

def create_access_token(user_id: str, email: str) -> str:
    """
    Cria um novo token de acesso JWT.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "sub": user_id,          # 'subject', padrão para identificar o usuário
        "email": email,
        "iat": now,              # 'issued at', quando o token foi criado
        "exp": now + timedelta(hours=JWT_EXPIRATION_HOURS), # 'expiration', quando expira
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# ==========================================================
# 🔎 LÓGICA DE LOGIN (MONGO)
# ==========================================================

async def verify_user_credentials(db: AsyncIOMotorDatabase, email: str, password: str) -> Optional[Dict]:
    """
    Verifica as credenciais do usuário no banco de dados MongoDB.
    Retorna um dicionário com dados do usuário e token em caso de sucesso, ou None.
    """
    try:
        # ✅ CORREÇÃO 1: Usar a coleção correta -> "usuarios"
        user = await db.usuarios.find_one({"email": email})
        
        if not user:
            return None # Usuário não encontrado

        # ✅ CORREÇÃO 2: Procurar por "senha_hash" ou "hashed_password"
        # Isso garante compatibilidade com os dados antigos e os novos.
        hashed_password = user.get("senha_hash") or user.get("hashed_password")
        
        if not hashed_password:
            return None # Usuário não possui senha cadastrada

        # Verifica se a senha fornecida corresponde ao hash armazenado
        if not verify_password(password, hashed_password):
            return None # Senha incorreta

        # Captura o ID do usuário com segurança
        user_id = user.get("_id")
        if not user_id:
            return None # Documento do usuário está malformado (sem _id)
        
        user_id_str = str(user_id)

        # Gera o token de acesso
        token = create_access_token(
            user_id=user_id_str,
            email=user.get("email")
        )

        # ✅ CORREÇÃO 3: Retornar um dicionário serializável e consistente
        # Garante que todos os campos essenciais sejam retornados.
        return {
            "id": user_id_str,
            "email": user.get("email"),
            "nome": user.get("nome"),
            "role": user.get("role", "user"), # Define um padrão caso não exista
            "ativo": user.get("ativo", True), # Define um padrão caso não exista
            "token": token
        }
        
    except Exception as e:
        # Em um ambiente de produção, seria melhor logar o erro em vez de imprimir.
        print(f"Erro interno ao processar login para {email}: {repr(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno no servidor ao processar o login."
        )


# backend/models/usuario.py
from datetime import datetime
from typing import List, Optional
from pydantic import EmailStr
from beanie import Document
from enum import Enum

# Enum de perfis de usuário
class PerfilUsuario(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

# Modelo MongoDB
class Usuario(Document):
    nome: str
    email: EmailStr
    senha_hash: str  # senha armazenada como hash
    perfil: PerfilUsuario
    permissoes: List[str] = []
    ativo: bool = True
    primeiro_login: bool = True
    criado_em: Optional[datetime] = datetime.utcnow()
    atualizado_em: Optional[datetime] = datetime.utcnow()

    class Settings:
        name = "usuarios"  # coleção no MongoDB
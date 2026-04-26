from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ===============================
# Perfis de usuário
# ===============================
class PerfilUsuario(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

# ===============================
# Permissões por perfil
# ===============================
PERMISSOES_POR_PERFIL = {
    PerfilUsuario.SUPER_ADMIN: ["read", "write", "delete", "admin"],
    PerfilUsuario.ADMIN: ["read", "write", "delete"],
    PerfilUsuario.USER: ["read"],
}

# ===============================
# Schemas Pydantic
# ===============================
class UserBase(BaseModel):
    nome: str
    email: EmailStr
    perfil: PerfilUsuario

class UsuarioCreateSchema(UserBase):
    senha: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str]
    email: Optional[EmailStr]
    perfil: Optional[PerfilUsuario]
    senha: Optional[str]

class UsuarioResponse(UserBase):
    id: str
    ativo: bool
    permissoes: List[str]

class UsuarioListResponse(BaseModel):
    usuarios: List[UsuarioResponse]

class TrocarSenhaRequest(BaseModel):
    usuario_id: str
    nova_senha: str

class AlterarSenhaRequest(BaseModel):
    senha_atual: str
    nova_senha: str
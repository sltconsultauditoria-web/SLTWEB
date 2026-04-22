# backend/schemas/__init__.py
"""
Schemas Pydantic para validação de dados
Centraliza e exporta todos os schemas do sistema
"""

# ==============================
# Documento
# ==============================
from .documento import (
    TipoDocumento,
    StatusDocumento,
    DocumentoBase,
    DocumentoCreate,
    DocumentoUpload,
    DocumentoResponse,
    DocumentoListResponse,
    DocumentoProcessamentoResult,
)

# ==============================
# Obrigação
# ==============================
from .obrigacao import (
    TipoObrigacao,
    StatusObrigacao,
    PrioridadeObrigacao,
    ObrigacaoBase,
    ObrigacaoCreate,
    ObrigacaoUpdate,
    ObrigacaoResponse,
    ObrigacaoListResponse,
)

# ==============================
# Empresa
# ==============================
from .empresa import (
    EmpresaBase,
    EmpresaCreate,
    EmpresaResponse,
)

# ==============================
# Usuário
# ==============================
from .usuario import (
    PerfilUsuario,
    PERMISSOES_POR_PERFIL,
    UserBase,
    UsuarioCreateSchema,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioListResponse,
    TrocarSenhaRequest,
    AlterarSenhaRequest,
)

# ==============================
# Exportações públicas
# ==============================
__all__ = [
    # Documento
    "TipoDocumento",
    "StatusDocumento",
    "DocumentoBase",
    "DocumentoCreate",
    "DocumentoUpload",
    "DocumentoResponse",
    "DocumentoListResponse",
    "DocumentoProcessamentoResult",

    # Obrigação
    "TipoObrigacao",
    "StatusObrigacao",
    "PrioridadeObrigacao",
    "ObrigacaoBase",
    "ObrigacaoCreate",
    "ObrigacaoUpdate",
    "ObrigacaoResponse",
    "ObrigacaoListResponse",

    # Empresa
    "EmpresaBase",
    "EmpresaCreate",
    "EmpresaResponse",

    # Usuário
    "PerfilUsuario",
    "PERMISSOES_POR_PERFIL",
    "UserBase",
    "UsuarioCreateSchema",
    "UsuarioUpdate",
    "UsuarioResponse",
    "UsuarioListResponse",
    "TrocarSenhaRequest",
    "AlterarSenhaRequest",
]
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

class Obrigacoes_empresaBase(BaseModel):
    id: Optional[str] = None
    nome: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Obrigacoes_empresaCreate(Obrigacoes_empresaBase):
    pass

class Obrigacoes_empresaUpdate(Obrigacoes_empresaBase):
    pass

class Obrigacoes_empresaSchema(Obrigacoes_empresaBase):
    mongo_id: Optional[str] = None  # para expor o _id convertido
    regime_tributario: Optional[List[str]] = None
    periodicidade: Optional[str] = None
    prazo_entrega: Optional[str] = None
    orgao_responsavel: Optional[str] = None
    sistema_canal: Optional[str] = None
    multa_atraso: Optional[str] = None
    descricao: Optional[str] = None
    objetivos: Optional[List[str]] = None
    estrutura: Optional[List[Any]] = None
    campos_tags: Optional[List[Any]] = None
    validacoes: Optional[List[str]] = None
    integracoes: Optional[List[str]] = None

    class Config:
        orm_mode = True
        extra = "allow"  # permite campos extras sem quebrar

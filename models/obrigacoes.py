from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Obrigacao(BaseModel):
    nome: str = Field(..., description="Nome da obrigação")
    regime_tributario: List[str] = Field(..., description="Regimes tributários aplicáveis")
    periodicidade: str = Field(..., description="Periodicidade da obrigação")
    prazo_entrega: str = Field(..., description="Prazo de entrega da obrigação")
    orgao_responsavel: str = Field(..., description="Órgão responsável pela obrigação")
    sistema_canal: str = Field(..., description="Sistema ou canal de entrega")
    multa_atraso: str = Field(..., description="Descrição da multa por atraso")
    descricao: str = Field(..., description="Descrição da obrigação")
    objetivos: List[str] = Field(..., description="Lista de objetivos da obrigação")
    estrutura: List[dict] = Field(..., description="Estrutura ou grupos de eventos da obrigação")
    campos_tags: List[dict] = Field(..., description="Campos e tags principais da obrigação")
    validacoes: List[str] = Field(..., description="Validações e regras de negócio")
    integracoes: List[str] = Field(..., description="Integrações e fluxo de dados")
    status: Optional[str] = Field("pendente", description="Status da obrigação (pendente, concluída, etc.)")
    data_criacao: date = Field(default_factory=date.today, description="Data de criação da obrigação")
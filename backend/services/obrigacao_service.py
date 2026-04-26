"""
Serviço de Obrigações Fiscais
Gerencia obrigações, vencimentos e alertas
"""

import uuid
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any, List
import logging

from motor.motor_asyncio import AsyncIOMotorDatabase
from fastapi.exceptions import HTTPException

from backend.schemas.obrigacao import (
    TipoObrigacao,
    StatusObrigacao,
    PrioridadeObrigacao,
    ObrigacaoCreate,
    ObrigacaoUpdate,
    ObrigacaoResponse
)
from backend.db.utils import mongo_list_to_dict_list

# Função utilitária para CNPJ (substitui import externo)
def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ removendo caracteres e garantindo 14 dígitos"""
    if not cnpj:
        return ""
    return "".join(filter(str.isdigit, cnpj)).zfill(14)

logger = logging.getLogger(__name__)


class ObrigacaoService:
    """
    Serviço para gerenciamento de obrigações fiscais
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db

    async def criar_obrigacao(self, dados: ObrigacaoCreate) -> ObrigacaoResponse:
        """
        Cria uma nova obrigação fiscal
        """
        logger.debug(f"Iniciando criação de obrigação com dados: {dados}")
        obrigacao_id = str(uuid.uuid4())

        prioridade = self._calcular_prioridade(dados.data_vencimento)

        obrigacao = {
            "id": obrigacao_id,
            "tipo": dados.tipo.value,
            "empresa_id": dados.empresa_id,
            "cnpj": formatar_cnpj(dados.cnpj),
            "competencia": dados.competencia,
            "ano": dados.ano,
            "mes": dados.mes,
            "valor": dados.valor,
            "valor_pago": 0.0,
            "data_vencimento": dados.data_vencimento.isoformat() if dados.data_vencimento else None,
            "data_pagamento": None,
            "status": StatusObrigacao.PENDENTE.value,
            "prioridade": prioridade.value,
            "documento_ids": [],
            "observacoes": dados.observacoes,
            "created_at": datetime.utcnow(),
            "updated_at": None
        }

        await self.db.obrigacoes.insert_one(obrigacao)

        # Buscar nome da empresa
        empresa = await self.db.empresas.find_one({"id": dados.empresa_id})
        if empresa:
            obrigacao["empresa_nome"] = empresa.get("razao_social") or empresa.get("nome_fantasia")

        return ObrigacaoResponse(**obrigacao)

    async def atualizar_obrigacao(
        self,
        obrigacao_id: str,
        dados: ObrigacaoUpdate
    ) -> Optional[ObrigacaoResponse]:
        """
        Atualiza uma obrigação existente
        """
        obrigacao = await self.db.obrigacoes.find_one({"id": obrigacao_id})
        if not obrigacao:
            return None

        update_data = {"updated_at": datetime.utcnow()}

        if dados.status is not None:
            update_data["status"] = dados.status.value
        if dados.valor is not None:
            update_data["valor"] = dados.valor
        if dados.data_vencimento is not None:
            update_data["data_vencimento"] = dados.data_vencimento.isoformat()
            update_data["prioridade"] = self._calcular_prioridade(dados.data_vencimento).value
        if dados.data_pagamento is not None:
            update_data["data_pagamento"] = dados.data_pagamento.isoformat()
            update_data["status"] = StatusObrigacao.CONCLUIDA.value
        if dados.prioridade is not None:
            update_data["prioridade"] = dados.prioridade.value
        if dados.observacoes is not None:
            update_data["observacoes"] = dados.observacoes

        await self.db.obrigacoes.update_one({"id": obrigacao_id}, {"$set": update_data})

        return await self.obter_obrigacao(obrigacao_id)

    async def obter_obrigacao(self, obrigacao_id: str) -> Optional[ObrigacaoResponse]:
        """
        Obtém uma obrigação pelo ID
        """
        obrigacao = await self.db.obrigacoes.find_one({"id": obrigacao_id}, {"_id": 0})
        if not obrigacao:
            return None

        # Converter datas
        if obrigacao.get("data_vencimento") and isinstance(obrigacao["data_vencimento"], str):
            obrigacao["data_vencimento"] = date.fromisoformat(obrigacao["data_vencimento"])
        if obrigacao.get("data_pagamento") and isinstance(obrigacao["data_pagamento"], str):
            obrigacao["data_pagamento"] = date.fromisoformat(obrigacao["data_pagamento"])

        # Buscar nome da empresa
        if obrigacao.get("empresa_id"):
            empresa = await self.db.empresas.find_one({"id": obrigacao["empresa_id"]})
            if empresa:
                obrigacao["empresa_nome"] = empresa.get("razao_social") or empresa.get("nome_fantasia")

        return ObrigacaoResponse(**obrigacao)

    async def listar_obrigacoes(
        self,
        empresa_id: Optional[str] = None,
        tipo: Optional[TipoObrigacao] = None,
        status: Optional[StatusObrigacao] = None,
        cnpj: Optional[str] = None,
        data_inicio: Optional[date] = None,
        data_fim: Optional[date] = None,
        pagina: int = 1,
        por_pagina: int = 20
    ) -> Dict[str, Any]:
        """
        Lista obrigações com filtros e paginação
        """
        filtro = {}

        if empresa_id:
            filtro["empresa_id"] = empresa_id
        if tipo:
            filtro["tipo"] = tipo.value
        if status:
            filtro["status"] = status.value
        if cnpj:
            filtro["cnpj"] = formatar_cnpj(cnpj)

        if data_inicio or data_fim:
            filtro["data_vencimento"] = {}
            if data_inicio:
                filtro["data_vencimento"]["$gte"] = data_inicio.isoformat()
            if data_fim:
                filtro["data_vencimento"]["$lte"] = data_fim.isoformat()

        total = await self.db.obrigacoes.count_documents(filtro)

        skip = (pagina - 1) * por_pagina
        cursor = self.db.obrigacoes.find(
            filtro,
            {"_id": 0}
        ).sort("data_vencimento", 1).skip(skip).limit(por_pagina)

        obrigacoes = await cursor.to_list(length=por_pagina)

        return {
            "obrigacoes": mongo_list_to_dict_list(obrigacoes),
            "total": total,
            "pagina": pagina,
            "por_pagina": por_pagina
        }

    async def obter_proximos_vencimentos(
        self,
        dias: int = 30,
        empresa_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Obtém obrigações com vencimento próximo
        """
        hoje = date.today()
        data_limite = hoje + timedelta(days=dias)

        filtro = {
            "status": {"$in": [StatusObrigacao.PENDENTE.value, StatusObrigacao.EM_ANDAMENTO.value]},
            "data_vencimento": {
                "$gte": hoje.isoformat(),
                "$lte": data_limite.isoformat()
            }
        }

        if empresa_id:
            filtro["empresa_id"] = empresa_id

        cursor = self.db.obrigacoes.find(
            filtro,
            {"_id": 0}
        ).sort("data_vencimento", 1)

        return await cursor.to_list(length=100)

    async def atualizar_status_atrasados(self) -> int:
        """
        Atualiza status de obrigações atrasadas
        """
        hoje = date.today().isoformat()

        result = await self.db.obrigacoes.update_many(
            {
                "status": {"$in": [StatusObrigacao.PENDENTE.value, StatusObrigacao.EM_ANDAMENTO.value]},
                "data_vencimento": {"$lt": hoje}
            },
            {
                "$set": {
                    "status": StatusObrigacao.ATRASADA.value,
                    "prioridade": PrioridadeObrigacao.CRITICA.value,
                    "updated_at": datetime.utcnow()
                }
            }
        )

        return result.modified_count

    def _calcular_prioridade(self, data_vencimento: Optional[date]) -> PrioridadeObrigacao:
        """
        Calcula prioridade baseada nos dias até vencimento
        """
        if not data_vencimento:
            return PrioridadeObrigacao.NORMAL

        dias = (data_vencimento - date.today()).days

        if dias < 0:
            return PrioridadeObrigacao.CRITICA
        if dias <= 3:
            return PrioridadeObrigacao.CRITICA
        if dias <= 7:
            return PrioridadeObrigacao.ALTA
        if dias <= 15:
            return PrioridadeObrigacao.NORMAL
        return PrioridadeObrigacao.BAIXA

    async def deletar_obrigacao(self, obrigacao_id: str) -> bool:
        """
        Deleta uma obrigação
        """
        result = await self.db.obrigacoes.delete_one({"id": obrigacao_id})
        return result.deleted_count > 0
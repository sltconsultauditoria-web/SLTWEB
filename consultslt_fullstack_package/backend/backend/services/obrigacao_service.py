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
from ajustar_cnpj_definitivo import formatar_cnpj

from backend.schemas.obrigacao import (
    TipoObrigacao,
    StatusObrigacao,
    PrioridadeObrigacao,
    ObrigacaoCreate,
    ObrigacaoUpdate,
    ObrigacaoResponse
)
from backend.db.utils import mongo_list_to_dict_list

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
        
        # Calcular prioridade baseada no vencimento
        prioridade = self._calcular_prioridade(dados.data_vencimento)
        
        # Formatar o CNPJ antes de salvar
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
        
        logger.debug(f"Dados da obrigação antes da inserção: {obrigacao}")
        await self.db.obrigacoes.insert_one(obrigacao)
        logger.debug("Obrigação inserida com sucesso no banco de dados.")
        
        # Buscar nome da empresa
        empresa = await self.db.empresas.find_one({"id": dados.empresa_id})
        if empresa:
            obrigacao["empresa_nome"] = empresa.get("razao_social") or empresa.get("nome_fantasia")
            logger.debug(f"Nome da empresa encontrado: {obrigacao['empresa_nome']}")
        else:
            logger.warning(f"Empresa com ID {dados.empresa_id} não encontrada.")
        
        return ObrigacaoResponse(**obrigacao)
    
    async def atualizar_obrigacao(
        self,
        obrigacao_id: str,
        dados: ObrigacaoUpdate
    ) -> Optional[ObrigacaoResponse]:
        """
        Atualiza uma obrigação existente
        """
        logger.debug(f"Iniciando atualização da obrigação com ID: {obrigacao_id}")
        obrigacao = await self.db.obrigacoes.find_one({"id": obrigacao_id})
        if not obrigacao:
            logger.warning(f"Obrigação com ID {obrigacao_id} não encontrada.")
            return None
        logger.debug(f"Dados atuais da obrigação: {obrigacao}")
        
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
        
        logger.debug(f"Dados para atualização: {update_data}")
        await self.db.obrigacoes.update_one({"id": obrigacao_id}, {"$set": update_data})
        logger.debug("Atualização concluída com sucesso.")
        
        # Retornar obrigação atualizada
        return await self.obter_obrigacao(obrigacao_id)
    
    async def obter_obrigacao(self, obrigacao_id: str) -> Optional[ObrigacaoResponse]:
        """
        Obtém uma obrigação pelo ID
        """
        obrigacao = await self.db.obrigacoes.find_one({"id": obrigacao_id}, {"_id": 0})
        if not obrigacao:
            return None
        
        # Converter datas de string para date
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
            filtro["cnpj"] = cnpj

        # Filtro por data de vencimento
        if data_inicio or data_fim:
            filtro["data_vencimento"] = {}
            if data_inicio:
                filtro["data_vencimento"]["$gte"] = data_inicio.isoformat()
            if data_fim:
                filtro["data_vencimento"]["$lte"] = data_fim.isoformat()

        logger.debug(f"Filtro aplicado: {filtro}")

        # Contar total
        try:
            total = await self.db.obrigacoes.count_documents(filtro)
            logger.debug(f"Total de obrigações encontradas: {total}")
        except Exception as e:
            logger.error(f"Erro ao contar documentos: {e}")
            raise

        # Buscar com paginação
        skip = (pagina - 1) * por_pagina
        logger.debug(f"Iniciando busca de obrigações com filtro: {filtro}")
        try:
            cursor = self.db.obrigacoes.find(
                filtro,
                {"_id": 0}  # Remover o campo '_id'
            ).sort("data_vencimento", 1).skip(skip).limit(por_pagina)

            obrigacoes = await cursor.to_list(length=por_pagina)
            logger.debug(f"Dados brutos retornados do MongoDB: {obrigacoes}")
        except Exception as e:
            logger.error(f"Erro ao buscar obrigações: {e}")
            raise HTTPException(status_code=500, detail="Erro ao buscar obrigações no banco de dados.")

        logger.debug("Iniciando tratamento dos dados retornados")
        for ob in obrigacoes:
            # Adiciona valores padrão para campos obrigatórios
            ob["id"] = ob.get("id", "")
            ob["empresa_id"] = ob.get("empresa_id", "")
            ob["tipo_obrigacao_id"] = ob.get("tipo_obrigacao_id", "")
            ob["tipo_codigo"] = ob.get("tipo_codigo", "DESCONHECIDO")
            ob["tipo_nome"] = ob.get("tipo_nome", "Desconhecido")
            ob["status"] = ob.get("status", StatusObrigacao.PENDENTE.value)
            ob["prioridade"] = ob.get("prioridade", PrioridadeObrigacao.NORMAL.value)
            ob["valor"] = ob.get("valor", 0.0)
            ob["valor_pago"] = ob.get("valor_pago", 0.0)
            ob["documento_ids"] = ob.get("documento_ids", [])
            ob["created_at"] = ob.get("created_at", datetime.utcnow())
            ob["updated_at"] = ob.get("updated_at", datetime.utcnow())

            # Converte datas para o formato correto
            if ob.get("data_vencimento") and isinstance(ob["data_vencimento"], str):
                try:
                    ob["data_vencimento"] = date.fromisoformat(ob["data_vencimento"])
                except ValueError:
                    logger.warning(f"Erro ao converter data_vencimento: {ob['data_vencimento']}")
                    ob["data_vencimento"] = None
            if ob.get("data_pagamento") and isinstance(ob["data_pagamento"], str):
                try:
                    ob["data_pagamento"] = date.fromisoformat(ob["data_pagamento"])
                except ValueError:
                    logger.warning(f"Erro ao converter data_pagamento: {ob['data_pagamento']}")
                    ob["data_pagamento"] = None
            if ob.get("ativo") and isinstance(ob["ativo"], dict):
                ob["ativo"] = True if ob["ativo"].get("$ifNull") else False

        logger.debug(f"Dados após tratamento: {obrigacoes}")

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
        Retorna quantidade de obrigações atualizadas
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
        
        if result.modified_count > 0:
            logger.info(f"{result.modified_count} obrigações marcadas como atrasadas")
        
        return result.modified_count
    
    def _calcular_prioridade(self, data_vencimento: Optional[date]) -> PrioridadeObrigacao:
        """
        Calcula prioridade baseada nos dias até o vencimento
        """
        if not data_vencimento:
            return PrioridadeObrigacao.NORMAL
        
        hoje = date.today()
        dias_ate_vencimento = (data_vencimento - hoje).days
        
        if dias_ate_vencimento < 0:
            return PrioridadeObrigacao.CRITICA  # Atrasada
        elif dias_ate_vencimento <= 3:
            return PrioridadeObrigacao.CRITICA
        elif dias_ate_vencimento <= 7:
            return PrioridadeObrigacao.ALTA
        elif dias_ate_vencimento <= 15:
            return PrioridadeObrigacao.NORMAL
        else:
            return PrioridadeObrigacao.BAIXA
    
    async def deletar_obrigacao(self, obrigacao_id: str) -> bool:
        """
        Deleta uma obrigação
        """
        result = await self.db.obrigacoes.delete_one({"id": obrigacao_id})
        return result.deleted_count > 0
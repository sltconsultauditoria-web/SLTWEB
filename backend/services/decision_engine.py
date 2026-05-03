from __future__ import annotations

from datetime import datetime
from typing import Any


class DecisionEngine:
    """Converte eventos em ações sugeridas e executáveis."""

    def analyze(self, event: dict[str, Any]) -> dict[str, Any]:
        origem = str(event.get("origem") or "").lower()
        tipo = str(event.get("tipo") or "").lower()
        severidade = str(event.get("severidade") or event.get("prioridade") or "media").lower()

        if tipo == "vencimento":
            acao = "regularizar"
            motivo = "Evento de vencimento exige regularização preventiva"
            executavel = True
        elif tipo == "erro":
            acao = "reprocessar_ocr"
            motivo = "Falha de processamento deve ser reprocessada"
            executavel = True
        elif tipo == "debito":
            acao = "consultar_e_cac"
            motivo = "Débito identificado pede validação na origem governamental"
            executavel = False
        elif tipo == "certidao":
            acao = "renovar_certidao"
            motivo = "Certidão vencendo ou vencida deve ser renovada"
            executavel = True
        else:
            acao = "revisar"
            motivo = f"Evento de origem {origem or 'indefinida'} requer avaliação"
            executavel = False

        prioridade = "alta" if severidade == "critica" else severidade
        return {
            "event_id": event.get("id") or event.get("_id"),
            "empresa_id": event.get("empresa_id"),
            "origem": origem,
            "tipo_evento": tipo,
            "severidade": severidade,
            "acao_sugerida": acao,
            "acao_automatica": executavel,
            "prioridade": prioridade,
            "motivo": motivo,
            "status": "pendente",
            "executado": False,
            "created_at": datetime.utcnow().isoformat(),
        }

    def execute(self, decision: dict[str, Any]) -> dict[str, Any]:
        return {
            **decision,
            "executado": True,
            "status": "executado",
            "executed_at": datetime.utcnow().isoformat(),
            "resultado": f"Ação '{decision.get('acao_sugerida')}' executada com sucesso",
        }


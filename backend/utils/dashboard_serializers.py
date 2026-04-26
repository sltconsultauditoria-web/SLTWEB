"""
Serialização do Dashboard (MongoDB -> JSON)
Separado para evitar circular imports
"""
from datetime import datetime
from typing import Dict, Any


def serialize_metric(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return {}

    return {
        "id": str(doc.get("_id", "")),
        "empresas_ativas": doc.get("empresas_ativas", 0),
        "empresas_inativas": doc.get("empresas_inativas", 0),
        "das_gerados_mes": doc.get("das_gerados_mes", 0),
        "certidoes_emitidas_mes": doc.get("certidoes_emitidas_mes", 0),
        "alertas_criticos": doc.get("alertas_criticos", 0),
        "taxa_conformidade": doc.get("taxa_conformidade", 0.0),
        "receita_bruta_mes": doc.get("receita_bruta_mes", 0.0),
        "despesa_mensal": doc.get("despesa_mensal", 0.0),
        "obrigacoes_pendentes": doc.get("obrigacoes_pendentes", 0),
        "proximos_vencimentos": doc.get("proximos_vencimentos", []),
        "atividades_recentes": doc.get("atividades_recentes", []),
        "data_geracao": (
            doc.get("data_geracao").isoformat()
            if isinstance(doc.get("data_geracao"), datetime)
            else doc.get("data_geracao")
        ),
        "data_atualizacao": (
            doc.get("data_atualizacao").isoformat()
            if isinstance(doc.get("data_atualizacao"), datetime)
            else doc.get("data_atualizacao")
        ),
        "ativo": doc.get("ativo", True)
    }


def serialize_snapshot(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return {}

    return {
        "id": str(doc.get("_id", "")),
        "data_snapshot": (
            doc.get("data_snapshot").isoformat()
            if isinstance(doc.get("data_snapshot"), datetime)
            else doc.get("data_snapshot")
        ),
        "metricas_json": doc.get("metricas_json", "{}"),
        "alteracoes": doc.get("alteracoes"),
        "criado_em": (
            doc.get("criado_em").isoformat()
            if isinstance(doc.get("criado_em"), datetime)
            else doc.get("criado_em")
        )
    }

from __future__ import annotations

import calendar
import re
from datetime import datetime, date, timedelta
from typing import Any


def _parse_competencia(competencia: str) -> tuple[int, int]:
    raw = str(competencia or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}", raw):
        year, month = raw.split("-")
        return int(year), int(month)
    if re.fullmatch(r"\d{2}/\d{4}", raw):
        month, year = raw.split("/")
        return int(year), int(month)
    if re.fullmatch(r"\d{4}", raw):
        return int(raw), 1
    raise ValueError("Competencia invalida")


def _last_business_day(year: int, month: int, day: int) -> date:
    day = min(day, calendar.monthrange(year, month)[1])
    current = date(year, month, day)
    while current.weekday() >= 5:
        current -= timedelta(days=1)
    return current


def _next_month(year: int, month: int) -> tuple[int, int]:
    if month == 12:
        return year + 1, 1
    return year, month + 1


def is_obrigacao_aplicavel(catalogo_item: dict[str, Any], regime: str, *, uf: str | None = None, cnae: str | None = None) -> bool:
    regimes = {str(item).strip().lower() for item in catalogo_item.get("regimes", [])}
    regime_norm = str(regime or "todos").strip().lower()
    if "todos" not in regimes and regime_norm not in regimes:
        return False
    uf_especifica = str(catalogo_item.get("uf_especifica") or "").strip().upper()
    if uf_especifica and uf and uf_especifica != uf.upper():
        return False
    if catalogo_item.get("codigo") == "PGDASD" and regime_norm != "simples_nacional":
        return False
    if catalogo_item.get("codigo") == "DEFIS" and regime_norm != "simples_nacional":
        return False
    if catalogo_item.get("codigo") == "EFDCONTRIB" and regime_norm not in {"lucro_real", "lucro_presumido"}:
        return False
    if catalogo_item.get("codigo") in {"SPEDECD", "SPEDECF", "DCTFMENSAL"} and regime_norm == "simples_nacional":
        return False
    return True


def calcular_vencimento(obrigacao: dict[str, Any], competencia: str, uf: str | None = None) -> date:
    year, month = _parse_competencia(competencia)
    prazo_dia = int(obrigacao.get("prazo_dia") or 15)
    periodicidade = str(obrigacao.get("periodicidade") or "mensal").lower()
    referencia_base = str(obrigacao.get("referencia_base") or "").lower()

    if periodicidade == "anual":
        due_year = year + 1 if referencia_base == "ano_anterior" else year
        due_month = int(obrigacao.get("prazo_mes") or 5)
        return _last_business_day(due_year, due_month, prazo_dia)

    if periodicidade == "eventual":
        base = date(year, month, 1)
        return base + timedelta(days=max(1, prazo_dia))

    if periodicidade == "mensal":
        due_year, due_month = _next_month(year, month)
        if obrigacao.get("uf_especifica") and uf and str(obrigacao.get("uf_especifica")).upper() == uf.upper():
            prazo_uf = obrigacao.get("prazos_uf") or {}
            if isinstance(prazo_uf, dict):
                uf_data = prazo_uf.get(str(uf).upper())
                if isinstance(uf_data, dict):
                    prazo_dia = int(uf_data.get("dia") or prazo_dia)
                    due_month = int(uf_data.get("mes") or due_month)
                    due_year = int(uf_data.get("ano") or due_year)
        vencimento = date(due_year, due_month, min(prazo_dia, calendar.monthrange(due_year, due_month)[1]))
        if obrigacao.get("antecipa_se_nao_util", True):
            while vencimento.weekday() >= 5:
                vencimento -= timedelta(days=1)
        return vencimento

    return date(year, month, min(prazo_dia, calendar.monthrange(year, month)[1]))


def calcular_status(
    vencimento: date | None,
    data_atual: date | None = None,
    *,
    entregue: bool = False,
    dispensada: bool = False,
    nao_aplicavel: bool = False,
) -> str:
    if nao_aplicavel:
        return "nao_aplicavel"
    if dispensada:
        return "dispensada"
    if entregue:
        return "entregue"
    if not vencimento:
        return "nao_aplicavel"
    hoje = data_atual or datetime.utcnow().date()
    if vencimento < hoje:
        return "atrasada"
    if vencimento == hoje:
        return "vence_hoje"
    if (vencimento - hoje).days <= 5:
        return "vencendo"
    return "em_dia"


def _build_alert_payload(obrigacao: dict[str, Any], days_left: int) -> dict[str, Any]:
    return {
        "empresa_id": obrigacao.get("empresa_id"),
        "obrigacao_codigo": obrigacao.get("obrigacao_codigo") or obrigacao.get("codigo_catalogo"),
        "competencia": obrigacao.get("competencia"),
        "vencimento": obrigacao.get("vencimento"),
        "prioridade": "alta" if days_left <= 5 else "media",
        "mensagem": f"{obrigacao.get('obrigacao_nome') or obrigacao.get('nome')} vence em {days_left} dia(s)",
        "status": "pendente",
    }


def gerar_alertas_vencimento(db, obrigacao: dict[str, Any], *, data_atual: date | None = None) -> dict[str, Any]:
    if not obrigacao.get("vencimento"):
        return {"created": 0}
    vencimento = date.fromisoformat(str(obrigacao["vencimento"]))
    hoje = data_atual or datetime.utcnow().date()
    days_left = (vencimento - hoje).days
    if days_left not in {10, 5, 1, 0, -1}:
        return {"created": 0}

    payload = _build_alert_payload(obrigacao, days_left)
    dedupe_key = f"alerta:{obrigacao.get('dedupe_key')}:{days_left}"
    payload["dedupe_key"] = dedupe_key
    existing = db["alertas"].find_one({"dedupe_key": dedupe_key})
    if existing:
        return {"created": 0}
    db["alertas"].insert_one({**payload, "created_at": datetime.utcnow().isoformat(), "updated_at": datetime.utcnow().isoformat()})
    db["eventos"].update_one(
        {"dedupe_key": f"evento:{dedupe_key}"},
        {"$set": {
            "dedupe_key": f"evento:{dedupe_key}",
            "tipo": "alerta",
            "empresa_id": obrigacao.get("empresa_id"),
            "obrigacao_codigo": obrigacao.get("obrigacao_codigo"),
            "competencia": obrigacao.get("competencia"),
            "prioridade": payload["prioridade"],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }},
        upsert=True,
    )
    return {"created": 1}

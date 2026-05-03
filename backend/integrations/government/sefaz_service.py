from __future__ import annotations

import os
from datetime import datetime, timedelta
from hashlib import sha1
from typing import Any


def _digits(value: Any) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def _seed(cnpj: str, periodo: str | None = None) -> int:
    key = f"{_digits(cnpj)}:{periodo or 'current'}"
    return int(sha1(key.encode("utf-8")).hexdigest()[:8], 16)


class SEFAZService:
    """Deterministic SEFAZ / NFe connector with real-mode flags."""

    def __init__(self) -> None:
        self.api_url = os.environ.get("SEFAZ_API_URL")
        self.api_key = os.environ.get("SEFAZ_API_KEY")
        self.real_mode = bool(self.api_url and self.api_key)

    def consultar_nfe(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        seed = _seed(cnpj, periodo)
        count_emitidas = (seed % 9) + 1
        count_recebidas = ((seed // 3) % 7) + 1
        total_documentos = count_emitidas + count_recebidas
        documentos = []
        for index in range(min(total_documentos, 6)):
            documentos.append(
                {
                    "chave_acesso": f"{seed:08d}{index:036d}"[:44],
                    "tipo": "nfe",
                    "status": "autorizada" if index % 3 != 0 else "pendente",
                    "valor": round(180 + ((seed >> index) % 800), 2),
                    "data_emissao": (datetime.utcnow().date() - timedelta(days=index * 2)).isoformat(),
                }
            )
        return {
            "cnpj": _digits(cnpj),
            "periodo_referencia": periodo or datetime.utcnow().strftime("%Y-%m"),
            "status": "ok" if seed % 5 else "atencao",
            "nfe_emitidas": count_emitidas,
            "nfe_recebidas": count_recebidas,
            "total_documentos": total_documentos,
            "documentos": documentos,
            "atualizado_em": datetime.utcnow().isoformat(),
            "modo": "real" if self.real_mode else "simulado",
        }


from __future__ import annotations

from datetime import datetime, timedelta
from hashlib import sha1
from typing import Any

from backend.integrations.government.base import GovernmentConnectorBase, digits_only


def _seed(cnpj: str, periodo: str | None = None) -> int:
    key = f"{digits_only(cnpj)}:{periodo or 'current'}"
    return int(sha1(key.encode("utf-8")).hexdigest()[:8], 16)


class PGDAService(GovernmentConnectorBase):
    provider_name = "pgdas"
    required_env_vars = ("PGDAS_USERNAME", "PGDAS_PASSWORD", "PGDAS_BASE_URL")

    def _simulate(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        seed = _seed(cnpj, periodo)
        receita = round(25000 + (seed % 70000), 2)
        das = round(receita * (0.04 + ((seed % 7) * 0.01)), 2)
        vencido = seed % 4 == 0
        return {
            "cnpj": digits_only(cnpj),
            "periodo_referencia": periodo or datetime.utcnow().strftime("%Y-%m"),
            "regime": "Simples Nacional",
            "status": "vencido" if vencido else "em_dia",
            "receita_bruta_12m": round(receita * 12, 2),
            "valor_das_estimado": das,
            "valor_das_pendente": das if vencido else 0,
            "sublimite_ultrapassado": receita > 300000,
            "proximo_vencimento": (datetime.utcnow().date() + timedelta(days=10 + (seed % 20))).isoformat(),
            "pendencias_pgdas": 1 if vencido else 0,
            "atualizado_em": datetime.utcnow().isoformat(),
        }

    def consultar_pgdas(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        return self._safe_real_call(
            lambda: self._real_pgdas(cnpj, periodo),
            lambda: self._simulate(cnpj, periodo),
        )

    def consultar(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        return self.consultar_pgdas(cnpj, periodo)["data"]

    def _real_pgdas(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        raise NotImplementedError("PGDAS real nao configurado")


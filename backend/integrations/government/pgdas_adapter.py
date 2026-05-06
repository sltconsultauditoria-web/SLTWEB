from __future__ import annotations

from typing import Any

from backend.integrations.government.pgdas_service import PGDAService


class PGDASAdapter:
    """Adapter de alto nivel para consulta PGDAS-D.

    A consulta real depende de compliance, credenciais e validação jurídica.
    """

    real_supported = False

    def __init__(self, service: PGDAService | None = None):
        self.service = service or PGDAService()

    def check_status(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        return self.service.consultar_pgdas(cnpj, periodo)

    def consultar_pgdas(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        return self.service.consultar_pgdas(cnpj, periodo)


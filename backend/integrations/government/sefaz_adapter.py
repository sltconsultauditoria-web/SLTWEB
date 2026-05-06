from __future__ import annotations

from typing import Any

from backend.integrations.government.sefaz_service import SEFAZService


class SEFAZAdapter:
    """Adapter de alto nivel para consultas NF-e/SEFAZ.

    O caminho real exige certificado ICP-Brasil, SOAP/XML assinado e parametrizacao por UF.
    """

    real_supported = False

    def __init__(self, service: SEFAZService | None = None):
        self.service = service or SEFAZService()

    def check_status(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        return self.service.consultar_nfe(cnpj, periodo)

    def consultar_nfe(self, cnpj: str, periodo: str | None = None) -> dict[str, Any]:
        return self.service.consultar_nfe(cnpj, periodo)


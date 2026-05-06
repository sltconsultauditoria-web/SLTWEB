from __future__ import annotations

from typing import Any

from backend.integrations.government.ecac_service import GovernmentECACService


class ECACAdapter:
    """Adapter de alto nivel para integração e-CAC.

    Mantém o contrato explícito entre modo real, simulado e not_configured.
    A implementação real depende de revisão jurídica, Gov.br, procuração e/ou RPA.
    """

    real_supported = False

    def __init__(self, service: GovernmentECACService | None = None):
        self.service = service or GovernmentECACService()

    def check_status(self, cnpj: str) -> dict[str, Any]:
        return self.service.consultar_status(cnpj)

    def consultar_debitos(self, cnpj: str) -> dict[str, Any]:
        return self.service.consultar_debitos(cnpj)

    def consultar_pendencias(self, cnpj: str) -> dict[str, Any]:
        return self.service.consultar_pendencias(cnpj)


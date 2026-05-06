from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CertificatePayload:
    certificate: bytes
    password: str | None = None
    source: str = "env"
    metadata: dict[str, Any] | None = None


class CertificateProvider(ABC):
    """Abstração para certificados digitais ICP-Brasil.

    A implementação de produção deve suportar rotação, auditoria e armazenamento seguro.
    """

    @abstractmethod
    def load(self) -> CertificatePayload | None:
        raise NotImplementedError


class EnvCertificateProvider(CertificateProvider):
    def load(self) -> CertificatePayload | None:
        cert = os.environ.get("CERTIFICADO_A1_BASE64")
        if not cert:
            return None
        return CertificatePayload(
            certificate=cert.encode("utf-8"),
            password=os.environ.get("CERTIFICADO_A1_PASSWORD"),
            source="env",
        )


class FileCertificateProvider(CertificateProvider):
    def __init__(self, path: str | None = None, password: str | None = None):
        self.path = Path(path or os.environ.get("CERTIFICADO_A1_PATH", ""))
        self.password = password or os.environ.get("CERTIFICADO_A1_PASSWORD")

    def load(self) -> CertificatePayload | None:
        if not self.path or not self.path.exists():
            return None
        return CertificatePayload(
            certificate=self.path.read_bytes(),
            password=self.password,
            source="file",
            metadata={"path": str(self.path)},
        )


class VaultCertificateProvider(CertificateProvider):
    def __init__(self, reference: str | None = None):
        self.reference = reference or os.environ.get("CERTIFICADO_VAULT_REF")

    def load(self) -> CertificatePayload | None:
        # Placeholder para integração futura com Vault/HSM.
        if not self.reference:
            return None
        return CertificatePayload(
            certificate=b"",
            source="vault",
            metadata={"reference": self.reference, "status": "not_implemented"},
        )

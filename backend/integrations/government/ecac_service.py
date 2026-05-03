from __future__ import annotations

from datetime import datetime, timedelta
from hashlib import sha1
from typing import Any

from backend.integrations.government.base import GovernmentConnectorBase, digits_only


def _seed(cnpj: str) -> int:
    digits = digits_only(cnpj) or "0"
    return int(sha1(digits.encode("utf-8")).hexdigest()[:8], 16)


class GovernmentECACService(GovernmentConnectorBase):
    provider_name = "ecac"
    required_env_vars = ("ECAC_CLIENT_ID", "ECAC_CLIENT_SECRET", "ECAC_BASE_URL")

    def _simulate_status(self, cnpj: str) -> dict[str, Any]:
        seed = _seed(cnpj)
        debitos_abertos = seed % 5
        certidoes_vencendo = (seed // 5) % 3
        score_risco = min(100, debitos_abertos * 18 + certidoes_vencendo * 20 + (seed % 11))
        situacao = "regular" if score_risco < 25 else "atencao" if score_risco < 60 else "critica"
        return {
            "cnpj": digits_only(cnpj),
            "status": "ok" if situacao == "regular" else "pendencia" if situacao == "atencao" else "critica",
            "situacao_fiscal": situacao,
            "debitos_abertos": debitos_abertos,
            "certidoes_vencendo": certidoes_vencendo,
            "score_risco": score_risco,
            "atualizado_em": datetime.utcnow().isoformat(),
        }

    def _simulate_debitos(self, cnpj: str) -> list[dict[str, Any]]:
        seed = _seed(cnpj)
        count = (seed % 3) + 1
        today = datetime.utcnow().date()
        items = []
        for index in range(count):
            amount = round(250.0 + ((seed >> index) % 800) + index * 97.5, 2)
            items.append(
                {
                    "id": f"ecac-debito-{index + 1}",
                    "cnpj": digits_only(cnpj),
                    "origem": "eCAC",
                    "tipo": "tributario",
                    "descricao": f"Debito federal simulado {index + 1}",
                    "valor": amount,
                    "vencimento": (today - timedelta(days=(index * 7) + (seed % 14))).isoformat(),
                    "status": "aberto" if index % 2 == 0 else "pendente",
                }
            )
        return items

    def _simulate_certidoes(self, cnpj: str) -> list[dict[str, Any]]:
        seed = _seed(cnpj)
        today = datetime.utcnow().date()
        return [
            {
                "tipo": "Federal (RFB/PGFN)",
                "cnpj": digits_only(cnpj),
                "status": "valida" if seed % 2 == 0 else "atencao",
                "data_emissao": datetime.utcnow().isoformat(),
                "data_validade": (today + timedelta(days=30 + (seed % 120))).isoformat(),
                "codigo_controle": f"CND-{seed % 999999:06d}",
            },
            {
                "tipo": "FGTS (CRF)",
                "cnpj": digits_only(cnpj),
                "status": "valida" if seed % 3 != 0 else "vencida",
                "data_emissao": datetime.utcnow().isoformat(),
                "data_validade": (today + timedelta(days=10 + (seed % 60))).isoformat(),
                "codigo_controle": f"CRF-{(seed // 3) % 999999:06d}",
            },
        ]

    def consultar_status(self, cnpj: str) -> dict[str, Any]:
        return self._safe_real_call(lambda: self._real_status(cnpj), lambda: self._simulate_status(cnpj))

    def consultar_debitos(self, cnpj: str) -> dict[str, Any]:
        return self._safe_real_call(lambda: self._real_debitos(cnpj), lambda: self._simulate_debitos(cnpj))

    def consultar_certidoes(self, cnpj: str) -> dict[str, Any]:
        return self._safe_real_call(lambda: self._real_certidoes(cnpj), lambda: self._simulate_certidoes(cnpj))

    def consultar_pendencias(self, cnpj: str) -> dict[str, Any]:
        return self._safe_real_call(lambda: self._real_pendencias(cnpj), lambda: self._simulate_pendencias(cnpj))

    def status(self, cnpj: str) -> dict[str, Any]:
        return self.consultar_status(cnpj)["data"]

    def debitos(self, cnpj: str) -> list[dict[str, Any]]:
        return self.consultar_debitos(cnpj)["data"]

    def certidoes(self, cnpj: str) -> list[dict[str, Any]]:
        return self.consultar_certidoes(cnpj)["data"]

    def pendencias(self, cnpj: str) -> dict[str, Any]:
        return self.consultar_pendencias(cnpj)["data"]

    def _simulate_pendencias(self, cnpj: str) -> dict[str, Any]:
        status = self._simulate_status(cnpj)
        return {
            "cnpj": status["cnpj"],
            "data_consulta": datetime.utcnow().isoformat(),
            "malha_fiscal": status["score_risco"] >= 60,
            "divida_ativa": status["debitos_abertos"] > 0,
            "caixa_postal_mensagens": status["debitos_abertos"] + 1,
            "pendencias_cadin": status["score_risco"] >= 40,
            "parcelamentos": {
                "ativos": max(0, status["debitos_abertos"] - 1),
                "em_atraso": 1 if status["score_risco"] >= 60 else 0,
            },
            "declaracoes_pendentes": {
                "dctf": status["score_risco"] // 40,
                "dctfweb": status["score_risco"] // 50,
                "efd_contribuicoes": status["score_risco"] // 60,
                "dirf": 0,
            },
            "score_risco": status["score_risco"],
            "nivel_risco": "CRITICO" if status["score_risco"] >= 70 else "ALTO" if status["score_risco"] >= 40 else "MEDIO" if status["score_risco"] >= 20 else "BAIXO",
            "modo": "real" if self.credentials_present() else "simulado",
        }

    def _real_status(self, cnpj: str) -> dict[str, Any]:
        raise NotImplementedError("e-CAC real nao configurado")

    def _real_debitos(self, cnpj: str) -> list[dict[str, Any]]:
        raise NotImplementedError("e-CAC real nao configurado")

    def _real_certidoes(self, cnpj: str) -> list[dict[str, Any]]:
        raise NotImplementedError("e-CAC real nao configurado")

    def _real_pendencias(self, cnpj: str) -> dict[str, Any]:
        raise NotImplementedError("e-CAC real nao configurado")


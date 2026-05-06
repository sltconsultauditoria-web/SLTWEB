from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Callable


def now() -> str:
    return datetime.utcnow().isoformat()


def digits_only(value: Any) -> str:
    return "".join(ch for ch in str(value or "") if ch.isdigit())


def mask_secret(value: str | None) -> str:
    if not value:
        return ""
    if len(value) <= 4:
        return "*" * len(value)
    return f"{value[:2]}***{value[-2:]}"


class GovernmentConnectorBase:
    provider_name = "base"
    required_env_vars: tuple[str, ...] = ()
    real_supported: bool = True

    def credentials_present(self) -> bool:
        return all(os.environ.get(name) for name in self.required_env_vars)

    def missing_env_vars(self) -> list[str]:
        return [name for name in self.required_env_vars if not os.environ.get(name)]

    def configured(self) -> bool:
        return self.credentials_present()

    def mode(self) -> str:
        if not self.credentials_present():
            return "not_configured"
        if not self.real_supported:
            return "simulado"
        return "real"

    def _contract(
        self,
        *,
        success: bool,
        data: dict[str, Any] | list[dict[str, Any]] | None,
        errors: list[str] | None = None,
        mode: str | None = None,
        status: str | None = None,
        message: str | None = None,
        next_action: str | None = None,
        configured: bool | None = None,
        missing_env_vars: list[str] | None = None,
        real_supported: bool | None = None,
    ) -> dict[str, Any]:
        resolved_mode = mode or self.mode()
        missing = self.missing_env_vars() if missing_env_vars is None else missing_env_vars
        resolved_configured = self.configured() if configured is None else configured
        resolved_real_supported = self.real_supported if real_supported is None else real_supported
        if message is None:
            if resolved_mode == "real":
                message = f"{self.provider_name} configurado e operando em modo real"
            elif resolved_mode == "simulado":
                message = f"{self.provider_name} operando em modo simulado"
            elif resolved_mode == "log_only":
                message = f"{self.provider_name} operando em modo log_only"
            else:
                message = f"{self.provider_name} nao configurado"
        if next_action is None:
            if resolved_mode == "real":
                next_action = "Manter observabilidade e credenciais validas"
            elif resolved_mode == "simulado":
                next_action = "Validar compliance e habilitar integracao real quando disponivel"
            elif resolved_mode == "log_only":
                next_action = "Configurar o provedor para sair de log_only"
            else:
                next_action = f"Configurar: {', '.join(missing) if missing else 'variaveis de ambiente'}"
        return {
            "success": success,
            "mode": resolved_mode,
            "modo": resolved_mode,
            "provider": self.provider_name,
            "data": data or {},
            "errors": errors or [],
            "configured": resolved_configured,
            "status": status or ("ok" if success else "error" if resolved_mode == "real" else resolved_mode),
            "message": message,
            "missing_env_vars": missing,
            "next_action": next_action,
            "real_supported": resolved_real_supported,
            "timestamp": now(),
        }

    def _safe_real_call(
        self,
        real_callable: Callable[[], dict[str, Any] | list[dict[str, Any]]],
        simulated_callable: Callable[[], dict[str, Any] | list[dict[str, Any]]],
    ) -> dict[str, Any]:
        if self.credentials_present():
            if not self.real_supported:
                return self._contract(
                    success=True,
                    data=simulated_callable(),
                    mode="simulado",
                    status="simulado",
                    message=f"{self.provider_name} preparado apenas para simulacao nesta build",
                    errors=["real_not_supported"],
                )
            try:
                data = real_callable()
                return self._contract(success=True, data=data, mode="real", status="ok")
            except Exception as exc:
                fallback = simulated_callable()
                return self._contract(
                    success=True,
                    data=fallback,
                    mode="simulado",
                    status="simulado",
                    message=f"{self.provider_name} real indisponivel; retornando simulacao",
                    errors=[f"fallback_simulado:{type(exc).__name__}"],
                )

        return self._contract(
            success=True,
            data=simulated_callable(),
            mode="not_configured" if not self.real_supported else "simulado",
            status="not_configured" if not self.credentials_present() else "simulado",
            message=f"{self.provider_name} nao configurado; retornando dados simulados",
        )


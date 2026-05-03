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

    def credentials_present(self) -> bool:
        return all(os.environ.get(name) for name in self.required_env_vars)

    def mode(self) -> str:
        return "real" if self.credentials_present() else "simulado"

    def _contract(
        self,
        *,
        success: bool,
        data: dict[str, Any] | list[dict[str, Any]] | None,
        errors: list[str] | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        return {
            "success": success,
            "mode": mode or self.mode(),
            "provider": self.provider_name,
            "data": data or {},
            "errors": errors or [],
            "timestamp": now(),
        }

    def _safe_real_call(
        self,
        real_callable: Callable[[], dict[str, Any] | list[dict[str, Any]]],
        simulated_callable: Callable[[], dict[str, Any] | list[dict[str, Any]]],
    ) -> dict[str, Any]:
        if self.credentials_present():
            try:
                data = real_callable()
                return self._contract(success=True, data=data, mode="real")
            except Exception as exc:
                fallback = simulated_callable()
                return self._contract(
                    success=True,
                    data=fallback,
                    mode="simulado",
                    errors=[f"fallback_simulado:{type(exc).__name__}"],
                )

        return self._contract(success=True, data=simulated_callable(), mode="simulado")


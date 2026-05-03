from __future__ import annotations

from typing import Any

from backend.services.email_service import public_smtp_config, send_email_notification


class EmailChannel:
    name = "email"

    def public_config(self) -> dict[str, Any]:
        return public_smtp_config()

    def send(self, notification: dict[str, Any], targets: list[str]) -> dict[str, Any]:
        payload = {**notification, "destinatarios": targets}
        result = send_email_notification(payload)
        return {
            "channel": self.name,
            "sent": bool(result.get("sent")),
            "mode": result.get("mode"),
            "reason": result.get("reason"),
            "targets": result.get("recipients") or targets,
        }

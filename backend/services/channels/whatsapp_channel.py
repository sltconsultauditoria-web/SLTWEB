from __future__ import annotations

import os
from typing import Any

from backend.services.channels.http_utils import post_json


class WhatsAppChannel:
    name = "whatsapp"

    def public_config(self) -> dict[str, Any]:
        return {
            "configured": bool(os.environ.get("WHATSAPP_API_URL") and os.environ.get("WHATSAPP_TOKEN")),
            "api_url": os.environ.get("WHATSAPP_API_URL", "").strip(),
            "token_configured": bool(os.environ.get("WHATSAPP_TOKEN")),
        }

    def send(self, notification: dict[str, Any], targets: list[str]) -> dict[str, Any]:
        api_url = os.environ.get("WHATSAPP_API_URL", "").strip()
        token = os.environ.get("WHATSAPP_TOKEN", "").strip()
        targets = [target for target in targets if target]
        if not targets:
            return {"channel": self.name, "sent": False, "mode": "skipped", "reason": "no_targets", "targets": []}
        if not api_url or not token:
            return {
                "channel": self.name,
                "sent": False,
                "mode": "log_only",
                "reason": "whatsapp_not_configured",
                "targets": targets,
            }

        failures = []
        for target in targets:
            response = post_json(
                api_url,
                {"to": target, "message": notification.get("mensagem") or notification.get("subject") or ""},
                headers={"Authorization": f"Bearer {token}"},
            )
            if not response.get("ok"):
                failures.append({"target": target, "status_code": response.get("status_code"), "error": response.get("error")})

        return {
            "channel": self.name,
            "sent": not failures,
            "mode": "http",
            "reason": "delivery_failed" if failures else None,
            "targets": targets,
            "failures": failures,
        }

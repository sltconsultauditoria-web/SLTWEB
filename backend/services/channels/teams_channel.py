from __future__ import annotations

import os
from typing import Any

from backend.services.channels.http_utils import post_json


class TeamsChannel:
    name = "teams"

    def public_config(self) -> dict[str, Any]:
        return {"configured": bool(os.environ.get("TEAMS_WEBHOOK_URL")), "webhook_configured": bool(os.environ.get("TEAMS_WEBHOOK_URL"))}

    def send(self, notification: dict[str, Any], targets: list[str]) -> dict[str, Any]:
        webhook_url = os.environ.get("TEAMS_WEBHOOK_URL", "").strip()
        if not targets:
            targets = ["default"]
        if not webhook_url:
            return {
                "channel": self.name,
                "sent": False,
                "mode": "log_only",
                "reason": "teams_not_configured",
                "targets": targets,
            }

        title = notification.get("subject") or "Notificacao ConsultSLT"
        message = notification.get("mensagem") or ""
        response = post_json(webhook_url, {"title": title, "text": message})
        return {
            "channel": self.name,
            "sent": bool(response.get("ok")),
            "mode": "webhook",
            "reason": None if response.get("ok") else "delivery_failed",
            "targets": targets,
            "status_code": response.get("status_code"),
        }

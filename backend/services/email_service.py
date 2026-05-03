from __future__ import annotations

import os
import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from typing import Any


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    user: str
    password: str
    from_email: str

    @property
    def configured(self) -> bool:
        return bool(self.host and self.port and self.from_email)


def load_smtp_config() -> SMTPConfig:
    port_raw = os.environ.get("SMTP_PORT", "587")
    try:
        port = int(port_raw)
    except (TypeError, ValueError):
        port = 587

    user = os.environ.get("SMTP_USER", "").strip()
    return SMTPConfig(
        host=os.environ.get("SMTP_HOST", "").strip(),
        port=port,
        user=user,
        password=os.environ.get("SMTP_PASS", ""),
        from_email=(os.environ.get("SMTP_FROM", "").strip() or user),
    )


def public_smtp_config() -> dict[str, Any]:
    config = load_smtp_config()
    return {
        "configured": config.configured,
        "host": config.host,
        "port": config.port,
        "user": config.user,
        "from_email": config.from_email,
        "tls": True,
    }


def build_email_body(notification: dict[str, Any]) -> str:
    lines = [
        str(notification.get("mensagem") or ""),
        "",
        f"Tipo: {notification.get('tipo') or '-'}",
        f"Prioridade: {notification.get('prioridade') or notification.get('severidade') or '-'}",
        f"Timestamp: {notification.get('timestamp') or '-'}",
    ]
    if notification.get("empresa_id"):
        lines.append(f"Empresa: {notification.get('empresa_id')}")
    if notification.get("source_id"):
        lines.append(f"Origem: {notification.get('source_id')}")
    return "\n".join(lines).strip()


def send_email_notification(notification: dict[str, Any]) -> dict[str, Any]:
    config = load_smtp_config()
    recipients = [str(item).strip() for item in notification.get("destinatarios") or [] if str(item).strip()]
    if not recipients:
        return {"sent": False, "mode": "skipped", "reason": "no_recipients", "recipients": []}
    if not config.configured:
        return {"sent": False, "mode": "log_only", "reason": "smtp_not_configured", "recipients": recipients}

    message = EmailMessage()
    message["Subject"] = str(notification.get("subject") or "Notificacao ConsultSLT")
    message["From"] = config.from_email
    message["To"] = ", ".join(recipients)
    message.set_content(build_email_body(notification))

    with smtplib.SMTP(config.host, config.port, timeout=20) as smtp:
        smtp.starttls()
        if config.user:
            smtp.login(config.user, config.password)
        smtp.send_message(message)

    return {"sent": True, "mode": "smtp", "reason": None, "recipients": recipients}

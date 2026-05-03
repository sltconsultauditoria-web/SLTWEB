from __future__ import annotations

from datetime import datetime
from typing import Any, Callable

from bson import ObjectId

from backend.services.channels import EmailChannel, SlackChannel, TeamsChannel, WhatsAppChannel


CHANNELS = {
    "email": EmailChannel(),
    "whatsapp": WhatsAppChannel(),
    "teams": TeamsChannel(),
    "slack": SlackChannel(),
}

PRIORITY_ORDER = {"baixa": 1, "media": 2, "normal": 2, "alta": 3, "alto": 3, "critica": 4, "critico": 4}
LOG_ONLY_REASONS = {
    "smtp_not_configured",
    "whatsapp_not_configured",
    "teams_not_configured",
    "slack_not_configured",
    "no_targets",
    "no_matching_preferences",
}


def now() -> str:
    return datetime.utcnow().isoformat()


def serialize(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if isinstance(value, dict):
        data = {key: serialize(item) for key, item in value.items()}
        if "_id" in data and "id" not in data:
            data["id"] = data["_id"]
        data.pop("_id", None)
        return data
    return value


def normalize_priority(value: Any) -> str:
    raw = str(value or "").strip().lower()
    mapping = {
        "critico": "critica",
        "critica": "critica",
        "critical": "critica",
        "alta": "alta",
        "high": "alta",
        "media": "media",
        "medium": "media",
        "baixa": "baixa",
        "low": "baixa",
    }
    return mapping.get(raw, raw or "media")


def priority_rank(value: Any) -> int:
    return PRIORITY_ORDER.get(normalize_priority(value), 2)


def get_notification_channels(db: Any) -> list[dict[str, Any]]:
    channels = []
    for name, channel in CHANNELS.items():
        config = channel.public_config()
        document = {
            "id": name,
            "name": name,
            "enabled": True,
            "configured": bool(config.get("configured")),
            "config": config,
            "updated_at": now(),
        }
        db["notification_channels"].update_one({"id": name}, {"$set": document}, upsert=True)
        channels.append(document)
    return channels


def default_preference_from_recipient(recipient: dict[str, Any]) -> dict[str, Any]:
    channels = []
    if recipient.get("notify_email", True):
        channels.append("email")
    if recipient.get("notify_whatsapp", False):
        channels.append("whatsapp")
    if recipient.get("notify_teams", False):
        channels.append("teams")
    if recipient.get("notify_slack", False):
        channels.append("slack")

    return {
        "id": str(recipient.get("id") or recipient.get("_id") or ObjectId()),
        "user_id": str(recipient.get("user_id") or recipient.get("usuario_id") or ""),
        "name": str(recipient.get("name") or recipient.get("nome") or "").strip(),
        "email": str(recipient.get("email") or "").strip(),
        "whatsapp": str(recipient.get("whatsapp") or recipient.get("telefone") or "").strip(),
        "slack_target": str(recipient.get("slack_target") or "default").strip(),
        "teams_target": str(recipient.get("teams_target") or "default").strip(),
        "ativo": bool(recipient.get("ativo", recipient.get("active", True))),
        "channels": channels or ["email"],
        "tipos_alerta": recipient.get("tipos_alerta") if isinstance(recipient.get("tipos_alerta"), list) else ["alerta", "evento"],
        "prioridade_minima": normalize_priority(recipient.get("prioridade_minima") or "media"),
        "horario_inicio": str(recipient.get("horario_inicio") or "00:00"),
        "horario_fim": str(recipient.get("horario_fim") or "23:59"),
        "created_at": recipient.get("created_at") or now(),
        "updated_at": now(),
    }


def list_notification_preferences(db: Any) -> list[dict[str, Any]]:
    stored = list(db["notification_preferences"].find({}).sort("created_at", -1))
    if stored:
        return [serialize(item) for item in stored]
    recipients = list(db["alerts_recipients"].find({}).sort("created_at", -1))
    return [default_preference_from_recipient(serialize(item)) for item in recipients]


def save_notification_preferences(db: Any, payload: Any) -> list[dict[str, Any]]:
    items = payload if isinstance(payload, list) else payload.get("preferences") or payload.get("data") or [payload]
    if not isinstance(items, list):
        raise ValueError("Lista de preferencias obrigatoria")

    saved = []
    for item in items:
        document = default_preference_from_recipient(item)
        document["id"] = str(item.get("id") or document["id"] or ObjectId())
        channels = item.get("channels")
        if isinstance(channels, list):
            document["channels"] = [str(channel).strip().lower() for channel in channels if str(channel).strip().lower() in CHANNELS]
        document["updated_at"] = now()
        db["notification_preferences"].update_one({"id": document["id"]}, {"$set": document}, upsert=True)
        saved.append(serialize(document))
    return saved


def is_within_allowed_hours(preference: dict[str, Any], current: datetime | None = None) -> bool:
    current_time = (current or datetime.utcnow()).strftime("%H:%M")
    start = str(preference.get("horario_inicio") or "00:00")
    end = str(preference.get("horario_fim") or "23:59")
    if start <= end:
        return start <= current_time <= end
    return current_time >= start or current_time <= end


def preference_accepts(preference: dict[str, Any], tipo: str, prioridade: str) -> bool:
    if not bool(preference.get("ativo", True)):
        return False
    tipos = preference.get("tipos_alerta") if isinstance(preference.get("tipos_alerta"), list) else ["alerta", "evento"]
    if tipo not in {str(item).strip().lower() for item in tipos}:
        return False
    if priority_rank(prioridade) < priority_rank(preference.get("prioridade_minima") or "media"):
        return False
    return is_within_allowed_hours(preference)


def notification_subject(tipo: str, prioridade: str, document: dict[str, Any]) -> str:
    title = document.get("titulo") or document.get("tipo") or "notificacao"
    return f"[ConsultSLT] {tipo.title()} {normalize_priority(prioridade).upper()}: {title}"


def build_notification(tipo: str, document: dict[str, Any], preferences: list[dict[str, Any]]) -> dict[str, Any]:
    prioridade = normalize_priority(document.get("prioridade") or document.get("severidade"))
    targets: dict[str, list[str]] = {channel: [] for channel in CHANNELS}
    accepted_preferences = [preference for preference in preferences if preference_accepts(preference, tipo, prioridade)]

    for preference in accepted_preferences:
        active_channels = preference.get("channels") if isinstance(preference.get("channels"), list) else ["email"]
        if "email" in active_channels and preference.get("email"):
            targets["email"].append(str(preference["email"]).strip())
        if "whatsapp" in active_channels and preference.get("whatsapp"):
            targets["whatsapp"].append(str(preference["whatsapp"]).strip())
        if "teams" in active_channels:
            targets["teams"].append(str(preference.get("teams_target") or "default").strip())
        if "slack" in active_channels:
            targets["slack"].append(str(preference.get("slack_target") or "default").strip())

    return {
        "subject": notification_subject(tipo, prioridade, document),
        "destinatarios": targets["email"],
        "targets": {channel: sorted(set(values)) for channel, values in targets.items()},
        "tipo": tipo,
        "prioridade": prioridade,
        "mensagem": str(document.get("descricao") or document.get("mensagem") or document.get("titulo") or "Nova notificacao"),
        "timestamp": now(),
        "empresa_id": document.get("empresa_id"),
        "source_id": str(document.get("id") or document.get("_id") or ""),
    }


def log_notification(db: Any, document: dict[str, Any]) -> dict[str, Any]:
    document = {**document, "created_at": document.get("created_at") or now()}
    result = db["notification_logs"].insert_one(document)
    document["_id"] = result.inserted_id
    return serialize(document)


def queue_notification_dispatch(
    db: Any,
    create_job: Callable[..., dict[str, Any]],
    tipo: str,
    document: dict[str, Any],
    *,
    max_attempts: int = 3,
) -> dict[str, Any] | None:
    preferences = list_notification_preferences(db)
    notification = build_notification(tipo, document, preferences)
    if not any(notification["targets"].values()):
        log_notification(
            db,
            {
                "status": "skipped",
                "mode": "log_only",
                "reason": "no_matching_preferences",
                "channel": "all",
                "targets": [],
                "tipo": tipo,
                "prioridade": notification["prioridade"],
                "subject": notification["subject"],
                "notification": notification,
            },
        )
        return None
    return create_job("notification_dispatch", {"notification": notification}, max_attempts=max_attempts)


def dispatch_notification(db: Any, job_id: str, notification: dict[str, Any]) -> dict[str, Any]:
    results = []
    targets_by_channel = notification.get("targets") if isinstance(notification.get("targets"), dict) else {}
    if not targets_by_channel and notification.get("destinatarios"):
        targets_by_channel = {"email": notification.get("destinatarios") or []}

    for channel_name, channel in CHANNELS.items():
        targets = [str(target).strip() for target in targets_by_channel.get(channel_name, []) if str(target).strip()]
        if not targets and channel_name not in {"teams", "slack"}:
            continue
        if not targets and channel_name in {"teams", "slack"} and channel_name not in targets_by_channel:
            continue

        result = channel.send(notification, targets)
        status = "success" if result.get("sent") else "skipped" if result.get("reason") in LOG_ONLY_REASONS else "error"
        log = log_notification(
            db,
            {
                "job_id": job_id,
                "status": status,
                "mode": result.get("mode"),
                "reason": result.get("reason"),
                "channel": channel_name,
                "targets": result.get("targets") or targets,
                "tipo": notification.get("tipo"),
                "prioridade": notification.get("prioridade") or notification.get("severidade"),
                "subject": notification.get("subject"),
                "notification": notification,
                "result": result,
            },
        )
        if channel_name == "email":
            db["email_logs"].insert_one(
                {
                    "job_id": job_id,
                    "status": "done" if status in {"success", "skipped"} else "error",
                    "mode": result.get("mode"),
                    "reason": result.get("reason"),
                    "subject": notification.get("subject"),
                    "destinatarios": result.get("targets") or targets,
                    "tipo": notification.get("tipo"),
                    "prioridade": notification.get("prioridade") or notification.get("severidade"),
                    "notification": notification,
                    "created_at": now(),
                    "duration_ms": 0,
                }
            )
        results.append({"channel": channel_name, "status": status, "log_id": log["id"], "result": result})

    return {"channels": results, "errors": [item for item in results if item["status"] == "error"]}

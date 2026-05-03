from __future__ import annotations

from datetime import datetime, timedelta
import hashlib
import json
import os
from time import perf_counter
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
RETRYABLE_REASONS = {"delivery_failed", "rate_limited"}
MAX_CHANNEL_ATTEMPTS = 3
RATE_LIMIT_DEFAULTS = {"email": 60, "whatsapp": 30}


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


def parse_iso_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        return value
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00").replace("+00:00", ""))
    except ValueError:
        return None


def mask_email(value: Any) -> str:
    email = str(value or "").strip()
    if "@" not in email:
        return email
    name, domain = email.split("@", 1)
    if len(name) <= 2:
        masked_name = name[:1] + "***"
    else:
        masked_name = f"{name[:2]}***{name[-1:]}"
    return f"{masked_name}@{domain}"


def mask_phone(value: Any) -> str:
    digits = "".join(ch for ch in str(value or "") if ch.isdigit())
    if len(digits) <= 4:
        return "***"
    return f"***{digits[-4:]}"


def mask_recipient(channel: str, recipient: Any) -> str:
    if channel == "email":
        return mask_email(recipient)
    if channel == "whatsapp":
        return mask_phone(recipient)
    if str(recipient or "") == "default":
        return "default"
    return "***"


def valid_recipient(channel: str, recipient: str) -> bool:
    if channel == "email":
        return "@" in recipient and "." in recipient.split("@")[-1]
    if channel == "whatsapp":
        return len("".join(ch for ch in recipient if ch.isdigit())) >= 10
    return bool(recipient)


def payload_hash(notification: dict[str, Any]) -> str:
    safe_payload = {
        "subject": notification.get("subject"),
        "tipo": notification.get("tipo"),
        "prioridade": notification.get("prioridade") or notification.get("severidade"),
        "mensagem": notification.get("mensagem"),
        "source_id": notification.get("source_id"),
    }
    encoded = json.dumps(safe_payload, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def idempotency_key(notification: dict[str, Any], channel: str, recipient: str) -> str:
    raw = "|".join(
        [
            str(notification.get("source_id") or notification.get("id") or notification.get("timestamp") or ""),
            str(notification.get("tipo") or ""),
            channel,
            recipient,
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def rate_limit_for(channel: str) -> int | None:
    env_name = f"NOTIFICATION_{channel.upper()}_RATE_LIMIT_PER_MIN"
    raw = os.environ.get(env_name)
    try:
        return int(raw) if raw else RATE_LIMIT_DEFAULTS.get(channel)
    except ValueError:
        return RATE_LIMIT_DEFAULTS.get(channel)


def channel_rate_limited(db: Any, channel: str) -> bool:
    limit = rate_limit_for(channel)
    if not limit:
        return False
    since = (datetime.utcnow() - timedelta(minutes=1)).isoformat()
    count = db["notification_logs"].count_documents({"channel": channel, "status": "success", "created_at": {"$gte": since}})
    return count >= limit


def next_retry_at(attempts: int) -> str:
    delay_seconds = min(300, 2 ** max(0, attempts - 1))
    return (datetime.utcnow() + timedelta(seconds=delay_seconds)).isoformat()


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


def create_internal_failure_alert(db: Any, channel: str, notification: dict[str, Any], reason: str) -> None:
    key = f"notification_failure|{channel}|{notification.get('source_id') or notification.get('timestamp') or notification.get('subject')}"
    existing = db["pipeline_events"].find_one({"dedupe_key": key})
    if existing:
        return
    event = {
        "id": str(ObjectId()),
        "origem": "notifications",
        "tipo": "notification_failure",
        "severidade": "critica",
        "status": "novo",
        "titulo": f"Falha repetida no canal {channel}",
        "descricao": f"Canal {channel} falhou apos {MAX_CHANNEL_ATTEMPTS} tentativas: {reason}",
        "referencia": notification.get("source_id") or notification.get("subject"),
        "dedupe_key": key,
        "payload": {"channel": channel, "reason": reason},
        "created_at": now(),
    }
    db["pipeline_events"].insert_one(event)
    db["alertas"].insert_one(
        {
            "titulo": event["titulo"],
            "descricao": event["descricao"],
            "prioridade": "critica",
            "status": "pendente",
            "lido": False,
            "resolvido": False,
            "evento_id": event["id"],
            "created_at": now(),
        }
    )


def notification_metrics(db: Any) -> dict[str, Any]:
    logs = list(db["notification_logs"].find({}))
    sent = [item for item in logs if item.get("status") == "success"]
    errors = [item for item in logs if item.get("status") == "error"]
    retrying = [item for item in logs if item.get("status") == "retrying"]
    durations = [int(item.get("duration_ms") or 0) for item in logs if int(item.get("duration_ms") or 0) > 0]
    channels = get_notification_channels(db)
    today = datetime.utcnow().date().isoformat()
    sent_today = [item for item in sent if str(item.get("created_at") or "").startswith(today)]
    total_terminal = len(sent) + len(errors)
    success_rate = 0 if total_terminal == 0 else round((len(sent) / total_terminal) * 100, 2)
    latest_errors = sorted(errors, key=lambda item: item.get("created_at") or "", reverse=True)[:5]
    return {
        "total_enviados": len(sent),
        "total_erros": len(errors),
        "total_retrying": len(retrying),
        "tempo_medio_envio": round(sum(durations) / len(durations), 2) if durations else 0,
        "canais_ativos": [item["name"] for item in channels if item.get("configured")],
        "ultimos_erros": [serialize(item) for item in latest_errors],
        "enviadas_hoje": len(sent_today),
        "falhas": len(errors),
        "taxa_sucesso": success_rate,
    }


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
    retrying = []
    hash_value = payload_hash(notification)
    targets_by_channel = notification.get("targets") if isinstance(notification.get("targets"), dict) else {}
    if not targets_by_channel and notification.get("destinatarios"):
        targets_by_channel = {"email": notification.get("destinatarios") or []}

    for channel_name, channel in CHANNELS.items():
        targets = [str(target).strip() for target in targets_by_channel.get(channel_name, []) if str(target).strip()]
        if not targets and channel_name not in {"teams", "slack"}:
            continue
        if not targets and channel_name in {"teams", "slack"} and channel_name not in targets_by_channel:
            continue

        for target in targets:
            key = idempotency_key(notification, channel_name, target)
            masked_target = mask_recipient(channel_name, target)
            previous_success = db["notification_logs"].find_one({"idempotency_key": key, "status": "success"})
            if previous_success:
                results.append({"channel": channel_name, "recipient": masked_target, "status": "skipped", "reason": "duplicate_success"})
                continue

            previous_attempts = list(db["notification_logs"].find({"idempotency_key": key}).sort("created_at", -1).limit(1))
            attempts = int(previous_attempts[0].get("attempts") or 0) + 1 if previous_attempts else 1
            started = perf_counter()

            if not valid_recipient(channel_name, target):
                result = {"channel": channel_name, "sent": False, "mode": "validation", "reason": "invalid_recipient", "targets": [masked_target]}
            elif channel_name in {"email", "whatsapp"} and channel_rate_limited(db, channel_name):
                result = {"channel": channel_name, "sent": False, "mode": "rate_limit", "reason": "rate_limited", "targets": [masked_target]}
            else:
                result = channel.send(notification, [target])

            duration_ms = int((perf_counter() - started) * 1000)
            reason = result.get("reason")
            if result.get("sent"):
                status = "success"
                retry_at = None
            elif reason in LOG_ONLY_REASONS:
                status = "skipped"
                retry_at = None
            elif reason in RETRYABLE_REASONS and attempts < MAX_CHANNEL_ATTEMPTS:
                status = "retrying"
                retry_at = next_retry_at(attempts)
            else:
                status = "error"
                retry_at = None
                if attempts >= MAX_CHANNEL_ATTEMPTS:
                    create_internal_failure_alert(db, channel_name, notification, str(reason or "delivery_failed"))

            safe_result = {**result, "targets": [masked_target]}
            log = log_notification(
                db,
                {
                    "job_id": job_id,
                    "idempotency_key": key,
                    "payload_hash": hash_value,
                    "status": status,
                    "mode": result.get("mode"),
                    "reason": reason,
                    "last_error": reason if status in {"error", "retrying"} else None,
                    "next_retry_at": retry_at,
                    "channel": channel_name,
                    "recipient": masked_target,
                    "targets": [masked_target],
                    "attempts": attempts,
                    "duration_ms": duration_ms,
                    "tipo": notification.get("tipo"),
                    "prioridade": notification.get("prioridade") or notification.get("severidade"),
                    "subject": notification.get("subject"),
                    "notification": {**notification, "targets": {}},
                    "result": safe_result,
                },
            )
            if channel_name == "email":
                db["email_logs"].insert_one(
                    {
                        "job_id": job_id,
                        "status": "done" if status in {"success", "skipped"} else status,
                        "mode": result.get("mode"),
                        "reason": reason,
                        "subject": notification.get("subject"),
                        "destinatarios": [masked_target],
                        "tipo": notification.get("tipo"),
                        "prioridade": notification.get("prioridade") or notification.get("severidade"),
                        "notification": {**notification, "targets": {}},
                        "created_at": now(),
                        "duration_ms": duration_ms,
                    }
                )
            item = {
                "channel": channel_name,
                "recipient": masked_target,
                "status": status,
                "log_id": log["id"],
                "next_retry_at": retry_at,
                "attempts": attempts,
                "result": safe_result,
            }
            results.append(item)
            if status == "retrying":
                retrying.append(item)

    return {
        "channels": results,
        "errors": [item for item in results if item["status"] == "error"],
        "retrying": retrying,
    }

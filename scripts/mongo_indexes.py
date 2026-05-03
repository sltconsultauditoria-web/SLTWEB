import os

from pymongo import ASCENDING, MongoClient


MONGO_URL = os.environ.get("MONGO_URL") or os.environ.get("MONGO_URI") or "mongodb://localhost:27017/consultslt_db"
DB_NAME = os.environ.get("DB_NAME") or "consultslt_db"


def main() -> None:
    client = MongoClient(MONGO_URL)
    db = client[DB_NAME]

    db["empresas"].create_index([("cnpj", ASCENDING)], name="idx_empresas_cnpj")
    db["usuarios"].create_index([("email", ASCENDING)], name="idx_usuarios_email", unique=True, sparse=True)
    db["documentos"].create_index([("empresa_id", ASCENDING)], name="idx_documentos_empresa_id")
    db["alertas"].create_index([("status", ASCENDING)], name="idx_alertas_status")
    db["pipeline_events"].create_index(
        [("status", ASCENDING), ("severidade", ASCENDING)],
        name="idx_pipeline_events_status_severidade",
    )
    db["notification_logs"].create_index(
        [("idempotency_key", ASCENDING)],
        name="idx_notification_logs_idempotency_key",
        unique=True,
        sparse=True,
    )
    db["jobs"].create_index([("status", ASCENDING)], name="idx_jobs_status")

    print(f"Indices MongoDB aplicados em {DB_NAME}")


if __name__ == "__main__":
    main()

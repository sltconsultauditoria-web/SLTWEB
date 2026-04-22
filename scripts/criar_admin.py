import os
from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime
import uuid

# Configurações
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "consultslt_db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

admin_email = "admin@empresa.com"
admin_password = "admin123"
admin_nome = "Administrador"
admin_role = "admin"

client = MongoClient(MONGODB_URL)
db = client[DATABASE_NAME]

now = datetime.utcnow()
entity_id = str(uuid.uuid4())

admin_doc = {
    "email": admin_email,
    "hashed_password": pwd_context.hash(admin_password),
    "role": admin_role,
    "nome": admin_nome,
    "ativo": True,
    "entity_id": entity_id,
    "version": 1,
    "created_at": now,
    "created_by": None,
    "valid_from": now,
    "valid_to": None,
    "previous_version_id": None,
    "criado_em": now,
    "ultimo_acesso": None,
    "permissoes": [
        "usuarios:criar", "usuarios:editar", "usuarios:remover", "usuarios:listar",
        "empresas:gerenciar", "documentos:gerenciar"
    ]
}

result = db.usuarios.insert_one(admin_doc)
print(f"Usuário admin criado com _id: {result.inserted_id}")
client.close()

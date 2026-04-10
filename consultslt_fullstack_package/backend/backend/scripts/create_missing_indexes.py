from pymongo import MongoClient

print("\n🚀 CRIANDO ÍNDICES RECOMENDADOS (SAFE MODE)\n")

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

indexes = {
    "debitos": ["cnpj", "status", "created_at"],
    "documentos_empresa": ["empresa_id", "status", "created_at"],
    "guias": ["empresa_id", "status", "created_at"],
    "certidoes_empresa": ["empresa_id", "created_at"],
    "alertas": ["empresa_id", "status", "created_at"],
    "fiscal_iris": ["cnpj", "empresa_id", "created_at"],
    "usuarios": ["email"],
    "empresas": ["created_at"],
}

for col, fields in indexes.items():

    collection = db[col]

    print(f"\n📦 {col}")

    existing_indexes = collection.index_information()

    for field in fields:

        index_name = f"{field}_1"

        if index_name in existing_indexes:

            print(f"   ⚠ índice já existe: {field}")

        else:

            collection.create_index(field)

            print(f"   ✔ índice criado: {field}")

print("\n🏁 Índices verificados com sucesso\n")
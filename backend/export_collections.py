import os
import json
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do MongoDB
MONGODB_URL = os.getenv("MONGODB_URL")
DB_NAME = os.getenv("DB_NAME")

# Conectar ao MongoDB
client = MongoClient(MONGODB_URL)
db = client[DB_NAME]

# Listar todas as coleções
collections = db.list_collection_names()

# Diretório de saída
output_dir = "exported_data"
os.makedirs(output_dir, exist_ok=True)

# Função para converter objetos não serializáveis
class JSONEncoderCustom(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()  # Converter datetime para string ISO 8601
        return super().default(obj)

# Exportar dados de cada coleção
for collection_name in collections:
    collection = db[collection_name]
    data = list(collection.find())

    # Remover o campo _id (ObjectId) para evitar problemas de serialização
    for document in data:
        document.pop("_id", None)

    # Salvar em um arquivo JSON
    output_file = os.path.join(output_dir, f"{collection_name}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4, cls=JSONEncoderCustom)

print(f"Exportação concluída. Dados salvos no diretório: {output_dir}")
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client["consultslt_db"]

print("\n📦 COLEÇÕES DO BANCO consultslt_db\n")

collections = db.list_collection_names()

for c in collections:
    count = db[c].count_documents({})
    print(f"{c}  -> {count} documentos")

print("\nTotal:", len(collections))
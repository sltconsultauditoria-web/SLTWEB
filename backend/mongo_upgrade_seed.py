
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["consultslt_db"]

for col in ["ocr_documentos", "ocr_logs"]:
    db[col].insert_one({"init": True})

print("Collections criadas")

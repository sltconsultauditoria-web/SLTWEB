
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["consultslt_db"]

cols = [
    "auditoria",
    "robots_jobs",
    "certidoes",
    "debitos"
]

for c in cols:
    db[c].insert_one({"created": True})
    print("ok", c)

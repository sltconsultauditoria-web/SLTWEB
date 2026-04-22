from backend.database import get_collection
from bson import ObjectId

collection = get_collection("guias")

def create(data: dict):
    return collection.insert_one(data)

def find_all():
    return list(collection.find())

def find_by_id(id: str):
    return collection.find_one({"_id": ObjectId(id)})

def update(id: str, data: dict):
    return collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": data}
    )

def delete(id: str):
    return collection.delete_one({"_id": ObjectId(id)})

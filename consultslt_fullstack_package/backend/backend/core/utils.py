
from bson import ObjectId

def serialize(doc):
    if not doc:
        return None
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

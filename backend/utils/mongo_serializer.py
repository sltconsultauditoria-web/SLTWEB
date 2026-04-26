

# ===== AUTO SERIALIZER INJECTED =====
from bson import ObjectId

def serialize_mongo(document):
    if document is None:
        return None

    if isinstance(document, list):
        return [serialize_mongo(doc) for doc in document]

    if isinstance(document, dict):
        doc = {}
        for key, value in document.items():
            if isinstance(value, ObjectId):
                doc["id" if key == "_id" else key] = str(value)
            else:
                doc[key] = value
        if "_id" in document:
            doc["id"] = str(document["_id"])
        return doc

    return document
# ===== END SERIALIZER =====

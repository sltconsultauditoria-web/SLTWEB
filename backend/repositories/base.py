
from bson import ObjectId
from backend.core.utils import serialize

class BaseRepository:

    def __init__(self, collection):
        self.collection = collection

    async def create(self, data: dict, tenant_id: str):
        data["tenant_id"] = tenant_id
        data["deleted"] = False
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def get_all(self, tenant_id: str, filters: dict = None):
        query = filters or {}
        query["tenant_id"] = tenant_id
        query["deleted"] = False

        docs = await self.collection.find(query).to_list(1000)
        return [serialize(d) for d in docs]

    async def get_by_id(self, id: str, tenant_id: str):
        doc = await self.collection.find_one({
            "_id": ObjectId(id),
            "tenant_id": tenant_id,
            "deleted": False
        })
        return serialize(doc)

    async def update(self, id: str, data: dict, tenant_id: str):
        await self.collection.update_one(
            {"_id": ObjectId(id), "tenant_id": tenant_id},
            {"$set": data}
        )
        return await self.get_by_id(id, tenant_id)

    async def delete(self, id: str, tenant_id: str):
        await self.collection.update_one(
            {"_id": ObjectId(id), "tenant_id": tenant_id},
            {"$set": {"deleted": True}}
        )
        return True

from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class BaseRepository:
    def __init__(self, db: AsyncIOMotorDatabase, collection_name: str):
        self.db = db
        self.collection = db[collection_name]

    async def find_all(self, limit: int = 100) -> List[Dict[str, Any]]:
        items = await self.collection.find().to_list(limit)
        for item in items:
            item["id"] = str(item["_id"])
            del item["_id"]
        return items

    async def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        item = await self.collection.find_one({"_id": ObjectId(item_id)})
        if item:
            item["id"] = str(item["_id"])
            del item["_id"]
        return item

    async def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        result = await self.collection.insert_one(data)
        data["id"] = str(result.inserted_id)
        return data

    async def update(self, item_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        await self.collection.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": data}
        )
        return await self.find_by_id(item_id)

    async def delete(self, item_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(item_id)})
        return result.deleted_count > 0
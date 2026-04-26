
from backend.database import get_collection
from backend.core.security import hash_password

async def seed():
    users = get_collection("users")
    existing = await users.find_one({"email": "admin@consultslt.com"})
    if existing:
        return

    await users.insert_one({
        "name": "Admin",
        "email": "admin@consultslt.com",
        "password": hash_password("admin123"),
        "tenant_id": "default",
        "role": "admin",
        "deleted": False
    })

import os

from motor.motor_asyncio import AsyncIOMotorClient


client: AsyncIOMotorClient = None
db = None


class _DatabaseProxy:
    def _db(self):
        global client, db
        if db is None:
            mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/consultslt_db")
            client = AsyncIOMotorClient(mongo_url)
            db = client.get_database()
        return db

    def __getitem__(self, name):
        return self._db()[name]

    def __getattr__(self, name):
        return getattr(self._db(), name)


_db_proxy = _DatabaseProxy()


async def init_db():
    global client, db
    mongo_url = os.environ.get("MONGO_URL", "mongodb://localhost:27017/consultslt_db")
    client = AsyncIOMotorClient(mongo_url)
    await client.admin.command("ping")
    db = client.get_database()
    print(f"INFO: MongoDB conectado ({mongo_url})")


async def close_db():
    global client
    if client:
        client.close()
        print("INFO: MongoDB desconectado")


def get_db():
    return db if db is not None else _db_proxy


def register_db_events(app):
    @app.on_event("startup")
    async def startup_db_client():
        await init_db()

    @app.on_event("shutdown")
    async def shutdown_db_client():
        await close_db()

from datetime import datetime
from bson import ObjectId
from .base import BaseRepository

class FiscalRepository(BaseRepository):

    @property
    def collection(self):
        return self.db.fiscal


from datetime import datetime
from bson import ObjectId


class Fiscal_dataRepository(BaseRepository):

    @property
    def collection(self):
        return self.db.fiscal_data

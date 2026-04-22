
from backend.database import get_collection
from backend.repositories.base import BaseRepository

class FiscalDataRepository(BaseRepository):
    def __init__(self):
        super().__init__(get_collection("fiscal_data"))


from backend.database import get_collection
from backend.repositories.base import BaseRepository

class EmpresasRepository(BaseRepository):
    def __init__(self):
        super().__init__(get_collection("empresas"))

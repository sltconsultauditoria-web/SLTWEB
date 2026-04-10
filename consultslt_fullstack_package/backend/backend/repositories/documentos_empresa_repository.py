
from backend.database import get_collection
from backend.repositories.base import BaseRepository

class DocumentosEmpresaRepository(BaseRepository):
    def __init__(self):
        super().__init__(get_collection("documentos_empresa"))


from backend.database import get_collection
from backend.repositories.base import BaseRepository

class ObrigacoesEmpresaRepository(BaseRepository):
    def __init__(self):
        super().__init__(get_collection("obrigacoes_empresa"))

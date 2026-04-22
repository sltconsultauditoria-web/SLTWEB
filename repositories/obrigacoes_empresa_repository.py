
from datetime import datetime
from bson import ObjectId


class Obrigacoes_empresaRepository(BaseRepository):

    @property
    def collection(self):
        return self.db.obrigacoes_empresa

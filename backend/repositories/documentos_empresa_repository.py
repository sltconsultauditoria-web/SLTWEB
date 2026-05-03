
from datetime import datetime
from bson import ObjectId


class Documentos_empresaRepository(BaseRepository):

    @property
    def collection(self):
        return self.db.documentos_empresa

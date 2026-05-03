
from datetime import datetime
from bson import ObjectId


class Certidoes_empresaRepository(BaseRepository):

    @property
    def collection(self):
        return self.db.certidoes_empresa

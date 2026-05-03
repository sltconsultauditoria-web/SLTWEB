
from datetime import datetime
from bson import ObjectId


class Dashboard_metricsRepository(BaseRepository):

    @property
    def collection(self):
        return self.db.dashboard_metrics

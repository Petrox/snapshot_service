from __future__ import annotations

from redis.client import Redis

from common.data.base_repository import BaseRepository
from common.utilities import datetime_now
from core.data_changed.sv.smart_vision_model import SmartVisionModel


class SmartVisionRepository(BaseRepository):
    def __init__(self, connection: Redis):
        super().__init__(connection, 'smart_visions:')

    def _get_key(self, key: str):
        return f'{self.namespace}{key}'

    def add(self, model: SmartVisionModel) -> int:
        key = self._get_key(model.id)
        model.created_at = datetime_now()
        dic = self.to_redis(model)
        return self.connection.hset(key, mapping=dic)

    def get(self, identifier: str) -> SmartVisionModel | None:
        key = self._get_key(identifier)
        dic = self.connection.hgetall(key)
        if not dic:
            return None
        model: SmartVisionModel = self.from_redis(SmartVisionModel(), dic)
        return model

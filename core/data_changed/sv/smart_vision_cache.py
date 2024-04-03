from __future__ import annotations

from redis.client import Redis

from common.utilities import logger
from core.data_changed.sv.smart_vision import SmartVision
from core.data_changed.sv.smart_vision_model import SmartVisionModel
from core.data_changed.sv.smart_vision_repository import SmartVisionRepository
from core.data_changed.source_cache import BaseCache, SourceCache


class SmartVisionCache(BaseCache):
    dic = {}

    def __init__(self, connection: Redis, source_cache: SourceCache):
        self.smart_vision_repository = SmartVisionRepository(connection)
        self.source_cache = source_cache

    @staticmethod
    def set_dict(dic: dict):
        SmartVisionCache.dic = dic

    def get(self, source_id: str) -> SmartVision | None:
        if source_id not in SmartVisionCache.dic:
            model = self.smart_vision_repository.get(source_id)
            if model is None:
                source_model = self.source_cache.get(source_id)
                if source_model is None:
                    logger.warning(f'source was not found for Smart Vision Model, Detection will not work for {source_id}')
                    return None
                model = SmartVisionModel().map_from(source_model)
                self.smart_vision_repository.add(model)
            SmartVisionCache.dic[source_id] = SmartVision().map_from(model)
        return SmartVisionCache.dic[source_id]

    def refresh(self, source_id: str) -> SmartVision | None:
        if source_id in SmartVisionCache.dic:
            SmartVisionCache.dic.pop(source_id)
        return self.get(source_id)

    def remove(self, source_id: str):
        SmartVisionCache.dic[source_id] = None

import os
from multiprocessing import Pool

from common.event_bus.event_handler import EventHandler
from common.utilities import crate_redis_connection, RedisDb, config
from core.data_changed.sv.smart_vision_cache import SmartVisionCache
from core.data_changed.source_cache import SourceCache
from core.event_handlers.channel_names import EventChannels
from core.filters.out_filters import OutFilters

_main_connection = crate_redis_connection(RedisDb.MAIN)
_event_bus_connection = crate_redis_connection(RedisDb.EVENTBUS)
_source_cache = SourceCache(_main_connection)
_smart_vision_cache = SmartVisionCache(_main_connection, _source_cache)
_out_filters = OutFilters(_smart_vision_cache)


# noinspection DuplicatedCode
class OutFilterEventHandler(EventHandler):
    def __init__(self, source_cache_dic: dict, smart_vision_cache_dic: dict):
        self.pool: Pool = None  # Pool(4)  # None
        _source_cache.set_dict(source_cache_dic)
        _smart_vision_cache.set_dict(smart_vision_cache_dic)

    def __enter__(self):
        self.pool = Pool(config.snapshot.process_count if config.snapshot.process_count > 0 else os.cpu_count())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pool is not None:
            self.pool.close()
            self.pool.join()
        return self

    def handle(self, dic: dict):
        if dic is None or dic['type'] != 'message':
            return

        self.pool.apply_async(_handle, args=(dic,))


def _handle(dic: dict):
    out_message = _out_filters.ok(dic)
    if out_message is not None:
        _event_bus_connection.publish(EventChannels.smcp_in, out_message.create_publish_dic())

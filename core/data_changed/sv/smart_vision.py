import datetime
import json
from typing import List
from datetime import timedelta
from shapely.geometry import Polygon

from core.data_changed.sv.smart_vision_model import SmartVisionModel
from core.filters.detections import DetectionBox


class SmartVision:
    def __init__(self):
        self.id: str = ''
        self.brand: str = ''
        self.name: str = ''
        self.address: str = ''
        self.created_at: str = ''
        self.selected_list: dict = {}
        self.zones_list: List[Polygon] = []
        self.masks_list: List[Polygon] = []
        self.start_time: timedelta = timedelta()
        self.end_time: timedelta = timedelta()
        self.time_in_enabled: bool = False
        self.separator = 'º'
        self.array_separator = '+'

    @staticmethod
    def __create_area(do: DetectionBox):
        x1, y1, x2, y2 = do.x1, do.y1, do.x2, do.y2
        return Polygon([(x1, y1), (x1, y2), (x2, y1), (x2, y2)])

    @staticmethod
    def __create_polygon(value: str, separator: str) -> Polygon | None:
        if len(value) == 0:
            return Polygon([])
        arr = value.split(separator)  # arr.length is always an even number
        arr_len = len(arr)
        if (arr_len % 2) != 0 or arr_len < 6:
            return None
        length = int(len(arr) / 2)
        index = 0
        points = []
        for j in range(length):
            x = float(arr[index])
            index += 1
            y = float(arr[index])
            index += 1
            points.append((x, y))
        return Polygon(points)

    def __create_polygon_list(self, line: str) -> List[Polygon]:
        ret: List[Polygon] = []
        if len(line) > 0:
            ret = []
            splits = line.split(self.array_separator)
            for split in splits:
                zone_list = self.__create_polygon(split, self.separator)
                if zone_list is not None:
                    ret.append(zone_list)
        return ret

    def is_in_zones(self, do: DetectionBox) -> bool:
        if len(self.zones_list) == 0:
            return True
        area = self.__create_area(do)
        for zone_list in self.zones_list:
            if zone_list.length == 0:
                continue
            if zone_list.intersects(area):
                return True
        return False

    def is_in_masks(self, do: DetectionBox) -> bool:
        if len(self.masks_list) == 0:
            return False
        area = self.__create_area(do)
        for mask_list in self.masks_list:
            if mask_list.length == 0:
                continue
            if mask_list.intersects(area):
                return True
        return False

    def is_selected(self, label: str) -> bool:
        return label in self.selected_list

    def check_threshold(self, label: str, threshold: float) -> bool:
        return threshold >= self.selected_list[label]

    def is_in_time(self) -> bool:
        if not self.time_in_enabled:
            return True
        now = datetime.datetime.now()
        now_time = timedelta(hours=now.hour, minutes=now.minute)
        return self.start_time <= now_time <= self.end_time

    @staticmethod
    def __int_try_parse(value) -> (bool, int):
        try:
            return True, int(value)
        except ValueError:
            return False, value

    @staticmethod
    def __get_time(time_text: str) -> (bool, timedelta):
        if len(time_text) == 0:
            return False, timedelta()
        splits = time_text.split(':')
        if len(splits) != 2:
            return False, timedelta()

        ok, hour = SmartVision.__int_try_parse(splits[0])
        if not ok:
            return False, timedelta()
        ok, minute = SmartVision.__int_try_parse(splits[1])
        if not ok:
            return False, timedelta()
        return True, timedelta(hours=hour, minutes=minute)

    def map_from(self, model: SmartVisionModel):
        self.id = model.id
        self.brand = model.brand
        self.name = model.name
        self.address = model.address
        self.created_at = model.created_at
        self.selected_list = json.loads(model.selected_list_json)
        self.zones_list = self.__create_polygon_list(model.zones_list)
        self.masks_list = self.__create_polygon_list(model.masks_list)
        self.time_in_enabled, self.start_time = self.__get_time(model.start_time)
        if self.time_in_enabled:
            self.time_in_enabled, self.end_time = self.__get_time(model.end_time)

        return self

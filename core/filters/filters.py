from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from common.data.source_model import MotionDetectionType, SourceModel
from common.utilities import logger
from core.data_changed.sv.smart_vision_cache import SmartVisionCache
from core.data_changed.prev_image_cache import PrevImageCache
from core.filters.messages import InMessage, OutMessage
from core.filters.detections import DetectionBox, DetectionResult
from core.motion_detector.base_motion_detector import BaseMotionDetector
from core.motion_detector.imagehash_detector import ImageHashDetector
from core.motion_detector.opencv_detector import OpenCVDetector
from core.motion_detector.psnr_detector import PsnrDetector


class Filter(ABC):
    def __init__(self, smart_vision_cache: SmartVisionCache):
        self.smart_vision_cache = smart_vision_cache
        self.source_cache = smart_vision_cache.source_cache

    @abstractmethod
    def ok(self, message: InMessage) -> bool:
        raise NotImplementedError('Filter.ok')


class TimeFilter(Filter):
    def __init__(self, smart_vision_cache: SmartVisionCache):
        super().__init__(smart_vision_cache)

    def ok(self, message: InMessage) -> bool:
        smart_vision = self.smart_vision_cache.get(message.source_id)
        if smart_vision is None:
            return True
        if not smart_vision.is_in_time():
            logger.warning(f'source({message.source_id}) was not in time between {smart_vision.start_time} and {smart_vision.end_time}')
            return False
        return True


class MotionDetectionFilter(Filter):
    def __init__(self, smart_vision_cache: SmartVisionCache, source_model: SourceModel, prev_img_cache: PrevImageCache):
        super().__init__(smart_vision_cache)
        self.__source_model = source_model
        self.__prev_img_cache = prev_img_cache
        self.__detection_boxes: List[DetectionBox] = []

    def _create_motion_detector(self, source_model: SourceModel) -> BaseMotionDetector | None:
        if source_model.md_type == MotionDetectionType.OpenCV:
            return OpenCVDetector(source_model, self.__prev_img_cache)
        elif source_model.md_type == MotionDetectionType.ImageHash:
            return ImageHashDetector(source_model, self.__prev_img_cache)
        elif source_model.md_type == MotionDetectionType.Psnr:
            return PsnrDetector(source_model, self.__prev_img_cache)
        else:
            logger.warning(f'Motion Detection Type was not found for source({source_model.id})')
            return None

    def ok(self, message: InMessage) -> bool:
        if self.__source_model.md_type == MotionDetectionType.NoMotionDetection:
            return True

        md: BaseMotionDetector | None = self._create_motion_detector(self.__source_model)
        if md is None:
            return False

        ret = md.has_motion(message.np_img)
        self.__detection_boxes = ret.detection_boxes
        return ret.has_motion

    def get_detection_boxes(self) -> List[DetectionBox]:
        return self.__detection_boxes


class ZoneFilter(Filter):
    def __init__(self, smart_vision_cache: SmartVisionCache, boxes: List[DetectionBox]):
        super().__init__(smart_vision_cache)
        self.boxes: List[DetectionBox] = boxes

    def ok(self, message: InMessage) -> bool:
        smart_vision = self.smart_vision_cache.get(message.source_id)
        if smart_vision is None:
            return True
        for box in self.boxes:
            if not smart_vision.is_in_zones(box):
                logger.warning(f'a object which was detected by source({message.source_id}) was in the specified zone')
                return False
        return True


class MaskFilter(Filter):
    def __init__(self, smart_vision_cache: SmartVisionCache, boxes: List[DetectionBox]):
        super().__init__(smart_vision_cache)
        self.boxes: List[DetectionBox] = boxes

    def ok(self, message: InMessage) -> bool:
        smart_vision = self.smart_vision_cache.get(message.source_id)
        if smart_vision is None:
            return True
        for box in self.boxes:
            if smart_vision.is_in_masks(box):
                logger.warning(f'a object which was detected by source({message.source_id}) was in the specified mask')
                return False
        return True


class ObjectDetectionFilter(Filter):
    def __init__(self, smart_vision_cache: SmartVisionCache):
        super().__init__(smart_vision_cache)

    def ok(self, out_message: OutMessage) -> bool:
        source_id = out_message.source_id
        smart_vision = self.smart_vision_cache.get(source_id)
        if smart_vision is None:
            logger.warning(f'no Object Detection record has been found for source({source_id})')
            return False

        if len(out_message.detections) == 0:
            return False

        filtered_list: List[DetectionResult] = []
        for d in out_message.detections:
            if not smart_vision.is_selected(d.label):
                logger.info(f'class index was not selected for source({source_id}) {d.label} ({d.score})')
                continue
            if not smart_vision.check_threshold(d.label, d.score):
                logger.info(f'threshold is lower then expected for source({source_id}) {d.label} ({d.score})')
                continue
            filtered_list.append(d)

        out_message.detections = filtered_list

        return len(filtered_list) > 0

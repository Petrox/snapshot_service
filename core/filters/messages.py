import base64
import json
from typing import List
import numpy as np
import numpy.typing as npt
from PIL import Image, UnidentifiedImageError
import io

from common.utilities import logger, datetime_now
from core.filters.detections import DetectionResult
from core.utilities import generate_id


class InMessage:
    def __init__(self):
        self.name: str = ''
        self.source_id: str = ''
        self.base64_image: str = ''
        self.np_img: npt.NDArray | None = None
        self.pil_image: Image = None
        self.ai_clip_enabled: bool = False
        self.encoding = 'utf-8'

    def form_dic(self, dic: dict) -> dict:
        data: bytes = dic['data']
        # todo: remove it if it is not necessary
        dic = json.loads(data.decode(self.encoding))
        self.name = dic['name']
        self.source_id = dic['source_id']
        self.base64_image = dic['base64_image']
        self.ai_clip_enabled = dic['ai_clip_enabled']

        base64_decoded = base64.b64decode(self.base64_image)
        try:
            self.pil_image = Image.open(io.BytesIO(base64_decoded))
            self.np_img = np.asarray(self.pil_image)
        except UnidentifiedImageError as err:
            logger.error(f'an error occurred while creating a PIL image from base64 string, err: {err}')

        return dic

    def create_publish_dic(self) -> str:
        dic = {'name': self.name, 'source_id': self.source_id, 'base64_image': self.base64_image, 'ai_clip_enabled': self.ai_clip_enabled}
        js = json.dumps(dic)
        return js


class OutMessage(InMessage):
    def __init__(self):
        super().__init__()
        self.module: str = ''
        self.detections: List[DetectionResult] = []

    def form_dic(self, dic: dict):
        dic = super(OutMessage, self).form_dic(dic)
        self.module = dic['module']
        ds = dic['detections']
        for d in ds:
            r = DetectionResult()
            r.module = self.module
            r.label = d['label']
            r.score = d['score']
            b = d['box']
            box = r.box
            box.x1 = b['x1']
            box.y1 = b['y1']
            box.x2 = b['x2']
            box.y2 = b['y2']
            self.detections.append(r)

    def create_publish_dic(self) -> str:
        ds = []
        for d in self.detections:
            b = d.box
            ds_item = {'label': d.label, 'score': d.score,
                       'box': {'x1': b.x1, 'y1': b.y1, 'x2': b.x2, 'y2': b.y2}}
            ds.append(ds_item)
        dic = {'id': generate_id(), 'module': self.module, 'source_id': self.source_id, 'created_at': datetime_now(),
               'detections': ds, 'base64_image': self.base64_image, 'ai_clip_enabled': self.ai_clip_enabled}
        # self.detections was already came form self.dic
        js = json.dumps(dic)
        return js

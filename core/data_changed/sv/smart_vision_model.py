from common.data.source_model import SourceModel


class SmartVisionModel:
    def __init__(self):
        self.id: str = ''
        self.brand: str = ''
        self.name: str = ''
        self.address: str = ''
        self.created_at: str = ''
        # todo: reflect changes to UI and other parts of the system
        self.selected_list_json: str = coco91class_json_as_string
        self.zones_list: str = ''
        self.masks_list: str = ''
        self.start_time: str = ''
        self.end_time: str = ''

    def map_from(self, source: SourceModel):
        self.id = source.id
        self.brand = source.brand
        self.name = source.name
        self.address = source.address
        return self


coco91class_json_as_string = """
{
  "person": 0.4,
  "bicycle": 0.4,
  "car": 0.4,
  "motorcycle": 0.4,
  "airplane": 0.4,
  "bus": 0.4,
  "train": 0.4,
  "truck": 0.4,
  "boat": 0.4,
  "traffic light": 0.4,
  "fire hydrant": 0.4,
  "street sign": 0.4,
  "stop sign": 0.4,
  "parking meter": 0.4,
  "bench": 0.4,
  "bird": 0.4,
  "cat": 0.4,
  "dog": 0.4,
  "horse": 0.4,
  "sheep": 0.4,
  "cow": 0.4,
  "elephant": 0.4,
  "bear": 0.4,
  "zebra": 0.4,
  "giraffe": 0.4,
  "hat": 0.4,
  "backpack": 0.4,
  "umbrella": 0.4,
  "shoe": 0.4,
  "eye glasses": 0.4,
  "handbag": 0.4,
  "tie": 0.4,
  "suitcase": 0.4,
  "frisbee": 0.4,
  "skis": 0.4,
  "snowboard": 0.4,
  "sports ball": 0.4,
  "kite": 0.4,
  "baseball bat": 0.4,
  "baseball glove": 0.4,
  "skateboard": 0.4,
  "surfboard": 0.4,
  "tennis racket": 0.4,
  "bottle": 0.4,
  "plate": 0.4,
  "wine glass": 0.4,
  "cup": 0.4,
  "fork": 0.4,
  "knife": 0.4,
  "spoon": 0.4,
  "bowl": 0.4,
  "banana": 0.4,
  "apple": 0.4,
  "sandwich": 0.4,
  "orange": 0.4,
  "broccoli": 0.4,
  "carrot": 0.4,
  "hot dog": 0.4,
  "pizza": 0.4,
  "donut": 0.4,
  "cake": 0.4,
  "chair": 0.4,
  "couch": 0.4,
  "potted plant": 0.4,
  "bed": 0.4,
  "mirror": 0.4,
  "dining table": 0.4,
  "window": 0.4,
  "desk": 0.4,
  "toilet": 0.4,
  "door": 0.4,
  "tv": 0.4,
  "laptop": 0.4,
  "mouse": 0.4,
  "remote": 0.4,
  "keyboard": 0.4,
  "cell phone": 0.4,
  "microwave": 0.4,
  "oven": 0.4,
  "toaster": 0.4,
  "sink": 0.4,
  "refrigerator": 0.4,
  "blender": 0.4,
  "book": 0.4,
  "clock": 0.4,
  "vase": 0.4,
  "scissors": 0.4,
  "teddy bear": 0.4,
  "hair drier": 0.4,
  "toothbrush": 0.4,
  "hair brush": 0.4
}
"""

class DetectionBox:
    def __init__(self):
        self.x1: int = 0
        self.y1: int = 0
        self.x2: int = 0
        self.y2: int = 0


class DetectionResult:
    def __init__(self):
        self.module: str = ''
        self.label: str = ''
        self.score: float = 0.0
        self.box: DetectionBox = DetectionBox()

    def format(self) -> str:
        return f'{self.label} {"{:.2f}".format(self.score)}'

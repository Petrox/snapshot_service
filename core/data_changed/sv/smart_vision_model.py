from common.data.source_model import SourceModel


class SmartVisionModel:
    def __init__(self):
        self.id: str = ''
        self.brand: str = ''
        self.name: str = ''
        self.address: str = ''
        self.created_at: str = ''
        # todo: reflect changes to UI and other parts of the system
        self.selected_list_json: str = '{"person":0.8}'
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

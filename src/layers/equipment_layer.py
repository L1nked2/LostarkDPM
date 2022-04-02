from engraving_layer import EngravingLayer
from utils import initialize_wrapper

class EquipmentLayer(EngravingLayer):
    @initialize_wrapper("EquipmentLayer", enable_start=False)
    def __init__(self, artifact_set, accessories, **kwargs):
        super(EquipmentLayer, self).__init__(**kwargs)
        self.artifact_set = artifact_set
        self.accessories = accessories
    
    # Overriding? or new method?
    def update(self):
        pass
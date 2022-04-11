from src.layers.static.engraving_layer import EngravingLayer
from src.layers.utils import initialize_wrapper, print_info_wrapper

class EquipmentLayer(EngravingLayer):
    layer_name = "EquipmentLayer"

    @initialize_wrapper("EquipmentLayer", enable_start=False)
    def __init__(self, artifact_set, accessories, **kwargs):
        super(EquipmentLayer, self).__init__(**kwargs)
        self.artifact_set = artifact_set
        self.accessories = accessories
    
    # Overriding? or new method?
    def update(self):
        pass
    
    @print_info_wrapper(layer_name)
    def print_equipment_info(self, detail=True):
        if detail:
            for attr_name in dir(self):
                if not attr_name.startswith("__"):
                    print(attr_name, getattr(self, attr_name))
        else:
            print("artifact set", self.artifact_set)
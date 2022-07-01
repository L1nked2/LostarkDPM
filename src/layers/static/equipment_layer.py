from src.layers.static.engraving_layer import EngravingLayer
from src.layers.utils import initialize_wrapper, print_info_wrapper

class EquipmentLayer(EngravingLayer):
    layer_name = "EquipmentLayer"

    @initialize_wrapper("EquipmentLayer", enable_start=False)
    def __init__(self, artifact_set, **kwargs):
        super(EquipmentLayer, self).__init__(**kwargs)
        artifact_raw_string = artifact_set
        self.artifact_set = self.parse_artifact_set(artifact_raw_string)
        self.apply_artifact_set()
        return

    def apply_artifact_set(self):
        
        return
    
    def parse_artifact_set(self, artifact_raw_string):
        artifact_set = dict()
        if len(artifact_raw_string) == 3:
            artifact_set['artifact_list'] = [artifact_raw_string[1:3]]
            artifact_set['artifact_count'] = [int(artifact_raw_string[0])]
        elif len(artifact_raw_string) == 6:
            artifact_set['artifact_list'] = [artifact_raw_string[1:3], artifact_raw_string[4:6]]
            artifact_set['artifact_count'] = [int(artifact_raw_string[0]), int(artifact_raw_string[3])]
        else:
            raise ValueError("Invalid artifact")
        return artifact_set
    
    @print_info_wrapper(layer_name)
    def print_equipment_info(self):
        print("artifact set", self.artifact_set)

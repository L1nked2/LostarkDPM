from src.layers.static.engraving_layer import EngravingLayer
from db.constants.common import ARTIFACT_TABLE
from src.layers.utils import initialize_wrapper, print_info_wrapper

class EquipmentLayer(EngravingLayer):
    layer_name = "EquipmentLayer"

    @initialize_wrapper("EquipmentLayer", enable_start=False)
    def __init__(self, artifact_set, **kwargs):
        super(EquipmentLayer, self).__init__(**kwargs)
        self.artifact_set = artifact_set
        self.apply_artifact_set()
        return

    def apply_artifact_set(self):
        for artifact in self.artifact_set:
          self.apply_one_artifact(artifact)
        return

    def apply_one_artifact(self, artifact):
      for target, effect in ARTIFACT_TABLE[artifact]:
        super(EngravingLayer, self).update_attribute_with_func(target, effect)
    
    @print_info_wrapper(layer_name)
    def print_equipment_info(self):
        print("artifact set:", self.artifact_set)

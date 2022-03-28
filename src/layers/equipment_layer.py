from engraving_layer import EngravingLayer

class EquipmentLayer(EngravingLayer):
    def __init__(self, artifact_set, accessories, **kwargs):
        super(EquipmentLayer, self).__init__(**kwargs)
        self.artifact_set_1 = artifact_set[0]
        self.artifact_set_2 = artifact_set[1]
        self.artifact_set_3 = artifact_set[2]
        self.accessories = accessories
    
    # Overriding? or new method?
    def update(self):
        pass
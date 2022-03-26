from engraving_layer import EngravingLayer

class EquipmentLayer(EngravingLayer):
    def __init__(self):
        super(EquipmentLayer, self).__init__()
        self.artifact_set_1 = ("악몽", 6)
        self.artifact_set_2 = None
        self.artifact_set_3 = None
    
    # Overriding? or new method?
    def update(self):
        pass
from character_layer import CharacterLayer

class EngravingLayer(CharacterLayer):
    def __init__(self):
        super(EngravingLayer, self).__init__()
        self.engraving_1 = ("원한", 3)
        self.engraving_2 = ("예둔", 3)
        self.engraving_3 = ("저받", 3)
        self.engraving_4 = ("질증", 3)
        self.engraving_5 = ("정흡", 3)
    
    # Overriding? or new method?
    def update(self):
        pass
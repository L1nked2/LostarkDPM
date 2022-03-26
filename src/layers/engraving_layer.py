from character_layer import CharacterLayer

class EngravingLayer(CharacterLayer):
    def __init__(self):
        super(EngravingLayer, self).__init__()
        self.engravings = [
            ("원한", 3),
            ("저받", 3),
            ("질증", 3),
            ("예둔", 3),
            ("정흡", 3)
        ]
        # self.engravings = engravings
    
    # Overriding? or new method?
    def update(self):
        pass
from character_layer import CharacterLayer

class EngravingLayer(CharacterLayer):
    def __init__(self, engravings, **kwargs):
        super(EngravingLayer, self).__init__(**kwargs)
        self.engravings = engravings
    
    # Overriding? or new method?
    def update(self):
        pass
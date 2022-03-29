from character_layer import CharacterLayer
from utils import initialize_wrapper


class EngravingLayer(CharacterLayer):
    @initialize_wrapper("EngravingLayer")
    def __init__(self, engravings, **kwargs):
        super(EngravingLayer, self).__init__(**kwargs)
        self.engravings = engravings
    
    # Overriding? or new method?
    def update(self):
        pass
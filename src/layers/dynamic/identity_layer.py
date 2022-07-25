# need to resolve ModuleNotFoundError later
from src.layers.static.character_layer import CharacterLayer
from src.classes.utils import class_by_name

class IdentityLayer:
    def __init__(self, character_info: CharacterLayer, class_name):
        print("hi")
        # InfoLayer class object
        self.character_info = character_info
        self.class_ = class_by_name(class_name)
        pass

    def fetch_identity_info(self):
        pass

    def apply_identity_info(self):
        pass
from src.layers.static.skill_tree_layer import SkillTreeLayer
from src.layers.utils import initialize_wrapper

# we may declare check list for each layer
# and aggregate them
STATIC_LAYER_CHECK_LIST = [
    "combat_stat",
    "attack_power",
    "engravings",
    "artifact_set",
    "skill_info"
]

class InfoLayer(SkillTreeLayer):
    
    @initialize_wrapper("InfoLayer", enable_start=False)
    def __init__(self, **kwargs):
        super(InfoLayer, self).__init__(**kwargs)
    
    def check_static_layer_initialization(self):
        for attribute_name in STATIC_LAYER_CHECK_LIST:
            try:
                attribute = getattr(self, attribute_name)
            except AttributeError as e:
                print(e)
            else:
                print(f"Attribute {attribute_name}: ", attribute)

    def print_layer_info(self, layers=["character", "engraving", "equipment", "skiltree"]):
        for layer in layers:
            print_info = getattr(self, "print" + layer + "info")
            print_info()

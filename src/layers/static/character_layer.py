from src.layers.static.equipment_layer import EquipmentLayer
from src.layers.utils import initialize_wrapper

# we may declare check list for each layer
# and aggregate them
STATIC_LAYER_CHECK_LIST = [
    "combat_stat",
    "attack_power",
    "engravings",
    "artifact_set",
]


class CharacterLayer(EquipmentLayer):
    layer_name = "CharacterLayer"
    @initialize_wrapper(layer_name, enable_start=False)
    def __init__(self, class_name, skill_set, **kwargs):
        super(CharacterLayer, self).__init__(**kwargs)
        self.class_name = class_name
        self.skill_set = skill_set

    def check_static_layer_initialization(self):
        for attribute_name in STATIC_LAYER_CHECK_LIST:
            try:
                attribute = getattr(self, attribute_name)
            except AttributeError as e:
                print(e)
            else:
                print(f"Attribute {attribute_name}: ", attribute)

    def print_layer_info(self, layers=["stat", "engraving", "equipment"]):
        for layer in layers:
            print_info = getattr(self, "print_" + layer + "_info")
            print_info()

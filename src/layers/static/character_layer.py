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
    
    def extract_dmg_stats(self):
        dmg_stats = dict()
        dmg_stats['attack_power'] = self.actual_attack_power
        dmg_stats['crit_rate'] = self.actual_crit_rate
        dmg_stats['crit_damage'] = self.crit_damage
        dmg_stats['total_multiplier'] = self.total_multiplier
        return dmg_stats

    def print_layer_info(self, layers=["stat", "engraving", "equipment"]):
        for layer in layers:
            print_info = getattr(self, "print_" + layer + "_info")
            print_info()

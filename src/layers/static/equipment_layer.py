from src.layers.static.engraving_layer import EngravingLayer
from src.layers.utils import initialize_wrapper, print_info_wrapper

class EquipmentLayer(EngravingLayer):
    layer_name = "EquipmentLayer"

    @initialize_wrapper("EquipmentLayer", enable_start=False)
    def __init__(self, artifact_set, **kwargs):
        super(EquipmentLayer, self).__init__(**kwargs)
        artifact_raw_string = artifact_set
        self.artifact_set = self.parse_artifact_set(artifact_raw_string)
        self.apply_artifact_set()
        return

    def apply_artifact_set(self):
        
        return
    
    def parse_artifact_set(self, artifact_raw_string):
        artifact_set = dict()
        if len(artifact_raw_string) == 3:
            artifact_set['artifact_list'] = [artifact_raw_string[1:3]]
            artifact_set['artifact_count'] = [int(artifact_raw_string[0])]
        elif len(artifact_raw_string) == 6:
            artifact_set['artifact_list'] = [artifact_raw_string[1:3], artifact_raw_string[4:6]]
            artifact_set['artifact_count'] = [int(artifact_raw_string[0]), int(artifact_raw_string[3])]
        else:
            raise ValueError("Invalid artifact")
        return artifact_set
    
    @print_info_wrapper(layer_name)
    def print_equipment_info(self):
        print("artifact set", self.artifact_set)

if __name__ == '__main__':
    
    stat = {
        'stat': 10000,
        'weapon_power': 10000,
        'combat_stat': {
            'crit': 1500,
            'specialization': 700,
            'domination': 0,
            'swiftness': 0,
            'endurance': 0,
            'expertise': 0
        }
    }
    # test CharacterLayer class methods
    temp = CharacterLayer(character_stat=stat)
    print("first details:")
    print(temp.get_character_detail())
    crit_rate_amount = 0.15
    crit_damage_amount = 0.5
    temp.update_attribute_with_func('crit_rate', lambda x: x + crit_rate_amount)
    temp.update_attribute_with_func('crit_damage', lambda x: x + crit_damage_amount)
    print("second details:")
    print(temp.get_character_detail())
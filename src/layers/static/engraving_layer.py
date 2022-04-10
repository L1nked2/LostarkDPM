from src.layers.static.character_layer import CharacterLayer
from src.layers.utils import initialize_wrapper, print_info_wrapper

class EngravingLayer(CharacterLayer):
    layer_name = "EngravingLayer"

    @initialize_wrapper("EngravingLayer", enable_start=False)
    def __init__(self, engravings, **kwargs):
        super(EngravingLayer, self).__init__(**kwargs)
        self.engravings = engravings
        self.apply_static_engravings()
    
    def apply_static_engravings(self):
        for engraving_dict in self.engravings:
            if engraving_dict['engraving_type'] == 'static':
                self.apply_one_engraving(engraving_dict)
                
    def apply_one_engraving(self, engraving_dict):
        for target, effect in zip(engraving_dict['engraving_target'], engraving_dict['engraving_effect']):
            super(EngravingLayer, self).update_attribute_with_func(target, effect)
    
    @print_info_wrapper(layer_name)
    def print_character_info(self, detail=True):
        if detail:
            for attr_name in dir(self):
                if not attr_name.startswith("__"):
                    print(attr_name, getattr(self, attr_name))
        else:
            print("engravings:", self.engravings)

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

    # Smaple shape of engraving configuration
    # It may include different values for each level of engraving
    engravings = [
        {
            'engraving_name': '원한',
            'engraving_type': 'static',
            'engraving_target': ['attack_power'],
            'engraving_effect': [(lambda x: x * 1.2)]
        },
        {
            'engraving_name': '저받',
            'engraving_type': 'static',
            'engraving_target': ['attack_power'],
            'engraving_effect': [(lambda x: x * 1.2)]
        },
        {
            'engraving_name': '정흡',
            'engraving_type': 'static',
            'engraving_target': ['attack_speed'],
            'engraving_effect': [(lambda x: x * 1.15)]
        },
        {
            'engraving_name': '예둔',
            'engraving_type': 'static',
            'engraving_target': ['crit_damage', 'additional_damage'],
            'engraving_effect': [(lambda x: x + 50), (lambda x: x - 0.03)]
        }
    ]

    temp = EngravingLayer(character_stat=stat, engravings=engravings)
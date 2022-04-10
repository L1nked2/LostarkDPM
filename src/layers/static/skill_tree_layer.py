from typing import List
from src.layers.static.equipment_layer import EquipmentLayer

from src.layers.utils import initialize_wrapper, print_info_wrapper
from src.layers.utils import json_parser

FROSTFIRE_JEWEL_LEVEL_DICT = {
    1: 3,
    2: 6,
    3: 9,
    4: 12,
    5: 15,
    6: 18,
    7: 21,
    8: 24,
    9: 30,
    10: 40
}

NEMESIS_JEWEL_LEVEL_DICT = {
    1: 2,
    2: 4,
    3: 6,
    4: 8,
    5: 10,
    6: 12,
    7: 14,
    8: 16,
    9: 18,
    10: 20
}

class Skill:
    def __init__(self, skill):
        self.damage = 0
        self.cooltime = 0
        self.tripod = None
        self.additional_attack_speed = 0

class SkilTreeLayer(EquipmentLayer):
    layer_name = "SkillTreeLayer"

    @initialize_wrapper("SkillTreeLayer", enable_start=False)
    def __init__(self, skill_tree, **kwargs):
        super(SkilTreeLayer, self).__init__(**kwargs)
        self.skill_tree = skill_tree
        self.skill_info : List[Skill] = None
        
        self.parse_skill_tree()
    
    def parse_skill_tree(self):
        json_content = json_parser(self.skill_tree)
        self.skill_buff_table = json_content["skill_buff_table"]
        self.skill_preset = json_content["skill_preset"]
        self.validate_skill_preset()
    
    def validate_skill_preset(self):
        # check the number of skills
        if len(self.skill_preset) > 8:
            raise Exception("Too many skills!")
    
    def get_skill_preset_by_name(self):
        if self.skill_preset is None:
            raise Exception("No skill preset initialized!")

        skill_list = []
        for skill in self.skill_preset:
            skill_list.append(skill["skill_name"])
        
        return skill_list
    
    def get_skill_preset_by_detail(self):
        pass

    def update_all_skill_info(self):
        pass
    
    @print_info_wrapper(layer_name)
    def print_character_info(self, detail=True):
        if detail:
            for attr_name in dir(self):
                if not attr_name.startswith("__"):
                    print(attr_name + ":", getattr(self, attr_name))
        else:
            print("skill info:", self.skill_info)
from typing import List
import warnings

from src.layers.static.equipment_layer import EquipmentLayer

from src.layers.utils import initialize_wrapper, print_info_wrapper
from src.layers.utils import json_parser

FROSTFIRE_JEWEL_LEVEL_DICT = {
    0: 0,
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
    0: 0,
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
        self.parse_skill_tree()
        self.save_skill_info()
    
    def parse_skill_tree(self):
        json_content = json_parser(self.skill_tree)
        self.skill_buff_table = json_content["skill_buff_table"]
        self.skill_preset = json_content["skill_preset"]
        self.validate_skill_preset()
    
    def validate_skill_preset(self):
        # check the number of skills
        if len(self.skill_preset) > 8:
            raise Exception("Too many skills!")

        num_skill_jewels = 0
        for skill in self.skill_preset:
            # validate skill name

            # validate skill rune

            # validate skill jewel
            skill_jewel = skill["skill_jewel"]
            if (0 < skill_jewel["frostfire"] <= 10):
                num_skill_jewels += 1
            
            if (0 < skill_jewel["nemesis"] <= 10):
                num_skill_jewels += 1
    
        if num_skill_jewels > 11:
            warnings.warn(f"LoasArkDPM expected less than or equal to 11 jewels, but detected {num_skill_jewels} jewels ...", UserWarning)
    
    def save_skill_info(self):
        # compute skill damage, cooltime
        # save it into Skill Class
        for skill in self.skill_preset:
            pass
    
    
    
    # @deprecate
    # def get_skill_preset_by_name(self):
    #     if self.skill_preset is None:
    #         raise Exception("No skill preset initialized!")

    #     skill_list = []
    #     for skill in self.skill_preset:
    #         skill_list.append(skill["skill_name"])
        
    #     return skill_list
    

    @print_info_wrapper(layer_name)
    def print_skilltree_info(self, detail=True):
        if detail:
            for attr_name in dir(self):
                if not attr_name.startswith("__"):
                    print(attr_name + ":", getattr(self, attr_name))
        else:
            print("skill info:", self.skill_info)
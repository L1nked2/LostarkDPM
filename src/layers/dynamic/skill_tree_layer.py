import warnings

from typing import List

from db.constants.common import COOLDOWN_PERCENTAGE_PER_SWIFTNESS
from db.constants.rune import get_rune_effect, validate_runes

from src.layers.static.equipment_layer import EquipmentLayer

from src.layers.utils import initialize_wrapper, print_info_wrapper
from src.layers.utils import json_parser

FROSTFIRE_JEWEL_LEVEL_DICT = {
    0: 0,
    1: 0.03,
    2: 0.06,
    3: 0.09,
    4: 0.12,
    5: 0.15,
    6: 0.18,
    7: 0.21,
    8: 0.24,
    9: 0.30,
    10: 0.40
}

NEMESIS_JEWEL_LEVEL_DICT = {
    0: 0,
    1: 0.02,
    2: 0.04,
    3: 0.06,
    4: 0.08,
    5: 0.10,
    6: 0.12,
    7: 0.14,
    8: 0.16,
    9: 0.18,
    10: 0.20
}

class SkillTreeLayer(EquipmentLayer):
    layer_name = "SkillTreeLayer"

    @initialize_wrapper("SkillTreeLayer", enable_start=False)
    def __init__(self, skill_tree, **kwargs):
        super(SkillTreeLayer, self).__init__(**kwargs)

        self.skill_tree = skill_tree
        self.skill_info: List[Skill] = []

        self.parse_skill_tree()
        self.save_skill_info()
    
    def parse_skill_tree(self):
        json_content = json_parser(self.skill_tree)
        self.skill_buff_table = json_content["skill_buff_table"]
        self.skill_preset = json_content["skill_preset"]
        self.validate_skill_preset()
    
    def validate_skill_preset(self):
        if len(self.skill_preset) > 8:
            raise Exception("Too many skills!")

        skill_runes = []
        num_skill_jewels = 0

        for skill in self.skill_preset:
            skill_runes.append(skill["skill_rune"])

            skill_jewel = skill["skill_jewel"]
            if (0 < skill_jewel["frostfire"] <= 10):
                num_skill_jewels += 1
            
            if (0 < skill_jewel["nemesis"] <= 10):
                num_skill_jewels += 1
    
        validate_runes(runes=skill_runes)

        if num_skill_jewels > 11:
            warnings.warn(f"LoasArkDPM expected less than or equal to 11 jewels, but detected {num_skill_jewels} jewels ...", UserWarning)
    
    def save_skill_info(self):
        for skill in self.skill_preset:
            skill_info = Skill(
                skill=skill,
                attack_power=self.attack_power_base,
                swiftness=self.combat_stat["swiftness"]
            )
            self.skill_info.append(skill_info)
            skill_info.print_skill_info()

    @print_info_wrapper(layer_name)
    def print_skilltree_info(self):
        print("skill info:", self.skill_info)
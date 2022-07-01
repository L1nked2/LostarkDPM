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

class Skill:
    def __init__(self, skill, attack_power, swiftness=0, **kwargs):
        self.name = skill["skill_name"]
        self.damage = []
        self.cooltime = skill["skill_attribute"]["쿨타임"]
        self.tripod_effects = []
        self.additional_attack_speed = 1

        self.compute_damage(skill, attack_power)
        self.save_tripods_to_effects(skill)
        self.compute_possible_static_info(skill, swiftness)

    def compute_damage(self, skill, attack_power):
        skill_default_damage = skill["skill_default_damage"]
        skill_default_coeff = skill["skill_default_coeff"]

        for idx, default in enumerate(skill_default_damage):
            result = default + attack_power * skill_default_coeff[idx]
            self.damage.append(result)
    
    def save_tripods_to_effects(self, skill):
        for i in [1, 2, 3]:
            tokenized_effects = [tuple(effect.split(" ")) for effect in skill[f"skill_tripod_{i}"]]
            self.tripod_effects.extend(tokenized_effects)

    def compute_possible_static_info(self, skill, swiftness):
        # Cooltime
        # e.g. ("cooltime", "+5"), ("cooltime", "-5")
        cooltime_effects = [effect for effect in self.tripod_effects if effect[0] == "cooltime"]

        for effect in cooltime_effects:
            self.cooltime += int(effect[1])
            if self.cooltime < 0:
                warnings.warn(f"Too much reducing cooltime, check skill configuration of {self.name}", UserWarning)
        
        self.cooltime *= (1 - swiftness * COOLDOWN_PERCENTAGE_PER_SWIFTNESS)

        # Frostfire jewel
        frostfire_level = skill["skill_jewel"]["frostfire"]
        for idx, damage in enumerate(self.damage):
            frostfired_damage = damage * (1 + FROSTFIRE_JEWEL_LEVEL_DICT[frostfire_level])
            self.damage[idx] = frostfired_damage

        # Nemesis jewel - to be considered here?

        # Additional attack speed
        ## Rune
        rune_category = skill["skill_rune"]["category"]
        rune_level = skill["skill_rune"]["level"]
        if rune_category == "질풍":
            self.additional_attack_speed *= (1 + get_rune_effect(category=rune_category, level=rune_level))

        ## Tripod
        attack_speed_effects = [effect for effect in self.tripod_effects if effect[1] == "공격속도"]
        for effect in attack_speed_effects:
            self.additional_attack_speed *= (1 + int(effect[2]) / 100)
    
    def print_skill_info(self):
        print(f"Name: {self.name}")
        print(f"Damage: {self.damage}")
        print(f"Cooltime: {self.cooltime}")


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
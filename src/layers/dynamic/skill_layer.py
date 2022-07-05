import warnings

from typing import List

from db.constants.common import COOLDOWN_PERCENTAGE_PER_SWIFTNESS
from db.constants.rune import get_rune_effect, validate_runes

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

class SkillLayer:
    layer_name = "SkillTreeLayer"

    @initialize_wrapper("SkillTreeLayer", enable_start=False)
    def __init__(self, skill_tree, **kwargs):
        self.remaining_cooldown = [0 for i in range(8)]

    @print_info_wrapper(layer_name)
    def print_skilltree_info(self):
        print("skill info:", self.skill_info)
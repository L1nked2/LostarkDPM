import warnings

from typing import List

from src.layers.static.constants import COOLDOWN_PERCENTAGE_PER_SWIFTNESS
from db.rune import get_rune_effect, validate_runes

from src.layers.utils import initialize_wrapper, print_info_wrapper
from src.layers.utils import json_parser



class SkillLayer:
    layer_name = "SkillTreeLayer"

    @initialize_wrapper("SkillTreeLayer", enable_start=False)
    def __init__(self, skill_tree, **kwargs):
        self.remaining_cooldown = [0 for i in range(8)]

    @print_info_wrapper(layer_name)
    def print_skilltree_info(self):
        print("skill info:", self.skill_info)
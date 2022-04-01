from equipment_layer import EquipmentLayer
from utils import initialize_wrapper
from utils import json_parser

class SkilTreeLayer(EquipmentLayer):
    @initialize_wrapper("SkillTreeLayer", enable_start=False)
    def __init__(self, skill_tree, **kwargs):
        super(SkilTreeLayer, self).__init__(**kwargs)
        self.skill_tree = skill_tree
        self.skill_cooldown_time = None
    
    def parse_skill_tree(self):
        json_content = json_parser(self.skill_tree)
        self.skill_buff_table = json_content["skill_buff_table"]
        self.skill_preset = json_content["skill_preset"]
        self.validate_skill_preset()
    
    def valiedate_skill_preset(self):
        pass

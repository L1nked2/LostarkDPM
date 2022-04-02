from equipment_layer import EquipmentLayer
from utils import initialize_wrapper
from utils import json_parser

class SkilTreeLayer(EquipmentLayer):
    @initialize_wrapper("SkillTreeLayer", enable_start=False)
    def __init__(self, skill_tree, **kwargs):
        super(SkilTreeLayer, self).__init__(**kwargs)
        self.skill_tree = skill_tree
        self.skill_cooldown_time = None
        
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

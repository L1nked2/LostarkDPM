from equipment_layer import EquipmentLayer
from utils import initialize_wrapper

class SkilTreeLayer(EquipmentLayer):
    @initialize_wrapper("SkillTreeLayer")
    def __init__(self, skill_tree, **kwargs):
        super(SkilTreeLayer, self).__init__(**kwargs)
        self.skill_tree = skill_tree
        self.skill_cooldown_time = None
    
    def parse_skill_tree(self):
        pass
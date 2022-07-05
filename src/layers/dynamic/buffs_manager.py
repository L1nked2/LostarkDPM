import importlib
from src.layers.dynamic.buff import StatBuff, SkillBuff, DamageBuff
from src.classes.base import BASE_BUFF_TABLE

class BuffsManager():
    def __init__(self, class_name, **kwargs):
        import_target = "src.classes." + class_name
        self.class_module = importlib.import_module(import_target)
        self.class_buff_table = getattr(self.class_module, 'CLASS_BUFF_TABLE')
        self.stat_buffs = list()
        self.skill_buffs = list()
        self.damage_buffs = list()

        self.reset_mutipliers()

    def reset_mutipliers(self):
        self.dynamic_multiplier = 1.0
        self.skill_dynamic_multiplier = 1.0
    
    def import_static_buffs(self, character):
        # Do something #
        pass

    def apply_stat_buffs(self, character):
        pass
    
    def apply_skill_buff(self, skill):
        pass
    
    def apply_damage_buff(self):
        pass
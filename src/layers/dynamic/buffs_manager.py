import importlib
from src.layers.dynamic.buff import StatBuff, SkillBuff, DamageBuff
from src.classes.base import BASE_BUFF_DICT
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.damage_history import DamageHistory

class BuffsManager():
    def __init__(self, class_name, **kwargs):
        import_target = "src.classes." + class_name
        self.class_module = importlib.import_module(import_target)
        self.base_buff_table = BASE_BUFF_DICT
        self.class_buff_table = getattr(self.class_module, 'CLASS_BUFF_DICT')
        self.current_buffs = list() 
        self.update_tick(0)

    def update_tick(self, tick):
        self.current_tick = tick
    
    def import_buffs(self, buffs_name_list):
        for buff_name in buffs_name_list:
          if buff_name in self.base_buff_table:
            self.register_buff(self.base_buff_table[buff_name])
          elif buff_name in self.class_buff_table:
            self.register_buff(self.class_buff_table[buff_name])
    
    def is_buff_exists(self, name):
        for buff in self.current_buffs:
          if buff.name == name:
            return True
        return False

    def register_buff(self, buff_dict):
        if self.is_buff_exists(buff_dict['name']):
            self.unregister_buff(buff_dict)
        if buff_dict['buff_type'] == 'stat':
          buff = StatBuff(**buff_dict, begin_tick=self.current_tick)
        elif buff_dict['buff_type'] == 'skill':
          buff = SkillBuff(**buff_dict, begin_tick=self.current_tick)
        elif buff_dict['buff_type'] == 'damage':
          buff = DamageBuff(**buff_dict, begin_tick=self.current_tick)
        else:
          raise Exception(f"BuffsManager: Wrong buff type, {buff_dict['type']}")
        self.current_buffs.append(buff)
    
    def unregister_buff(self, buff):
        for registerd_buff in self.current_buffs:
          if registerd_buff.name == buff['name']:
            self.current_buffs.remove(registerd_buff)
    
    def sort_buffs(self):
        self.current_buffs = sorted(self.current_buffs, key=lambda x: x.priority)
    
    def apply_stat_buffs(self, character: CharacterLayer):
        for buff in self.current_buffs:
            if buff.buff_type == 'stat':
                buff.apply_stat_buff(character)
    
    def apply_skill_buffs(self, skill):
        for buff in self.current_buffs:
            if buff.buff_type == 'skill':
                buff.apply_skill_buff(skill)
    
    def apply_damage_buffs(self, character: CharacterLayer, damage_history: DamageHistory):
        for buff in self.current_buffs:
            if buff.buff_type == 'damage':
                buff.apply_damage_buff(character, damage_history)

    def print_buffs(self):
        for buff in self.current_buffs:
            print(buff)
import importlib
import warnings
from src.layers.dynamic.buff import StatBuff, DamageBuff
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.damage_history import DamageHistory


class BuffManager():
    def __init__(self, base_character: CharacterLayer, verbose=False, **kwargs):
        self.base_character = base_character
        self.verbose = verbose
        self.base_buff_module = importlib.import_module("src.classes.base")
        import_target = "src.classes." + self.base_character.class_name
        self.class_buff_module = importlib.import_module(import_target)
        self.class_buff_table = self.class_buff_module.CLASS_BUFF_DICT
        self.current_buffs = list()
        self.update_tick(0)
        
        self._import_buffs(self.base_character.static_buff_queue)

        print('##### Done Initialization of BuffsManager #####')

    def update_tick(self, tick):
        self.current_tick = tick
        self._remove_expired_buffs()
    
    def _import_buffs(self, buffs_name_list):
        # register base buffs(default buffs)
        for buff_name in self.base_buff_module.BASE_BUFF_DICT:
            self.register_buff(self.base_buff_module.BASE_BUFF_DICT[buff_name], 'base')
        self.register_buff(self.class_buff_table['Specialization'], 'class')

        for buff_name in buffs_name_list:
          if buff_name in self.base_buff_module.COMMON_BUFF_DICT:
            self.register_buff(self.base_buff_module.COMMON_BUFF_DICT[buff_name], 'base')
          elif buff_name in self.class_buff_table:
            self.register_buff(self.class_buff_table[buff_name], 'class')
          else:
            warnings.warn(f'Not implemented buff detected, {buff_name}', UserWarning)
    
    def is_buff_exists(self, name):
        for buff in self.current_buffs:
          if buff.name == name:
            return True
        return False

    def register_buff(self, buff_dict, buff_origin):
        if self.is_buff_exists(buff_dict['name']):
            buff_name = buff_dict['name']
            if self.verbose:
              print(f'buff already exists, {buff_name} will be shadowed or refreshed')
            self._remove_redundant_buff(buff_dict)
        if buff_dict['buff_type'] == 'stat':
          buff = StatBuff(**buff_dict, buff_origin=buff_origin, begin_tick=self.current_tick)
        elif buff_dict['buff_type'] == 'damage':
          buff = DamageBuff(**buff_dict, buff_origin=buff_origin, begin_tick=self.current_tick)
        else:
          raise Exception(f"BuffsManager: Wrong buff type, {buff_dict['type']}")
        self.current_buffs.append(buff)
        self._shadow_buffs(buff.name)
    
    def unregister_buff(self, buff_name):
        for registerd_buff in self.current_buffs:
          if registerd_buff.name == buff_name:
            self.current_buffs.remove(registerd_buff)
    
    def apply_stat_buffs(self, character: CharacterLayer, skill: Skill):
        self._sort_buffs()
        for buff in self.current_buffs:
            if not buff.buff_type =='stat' or buff.is_shadowed:
                continue
            if buff.buff_origin == 'base':
                buff_body = getattr(self.base_buff_module, buff.effect)
            elif buff.buff_origin == 'class':
                buff_body = getattr(self.class_buff_module, buff.effect)
            buff_body(character, skill)
        skill.buff_applied = True
    
    ## TODO
    def apply_damage_buffs(self, character: CharacterLayer, damage_history: DamageHistory):
        for buff in self.current_buffs:
            if buff.buff_type == 'damage':
                buff.apply_damage_buff(character, damage_history)

    def print_buffs(self):
        print(self.current_buffs)

    # sort buffs by priority, decending order
    def _sort_buffs(self):
        self.current_buffs = sorted(self.current_buffs, key=lambda x: x.priority, reverse=True)

    def _remove_expired_buffs(self):
      removed_buffs = list()
      for buff in self.current_buffs:
        if buff.is_expired(self.current_tick) == True:
          removed_buffs.append(buff.name)
          self.current_buffs.remove(buff)
      for buff_name in removed_buffs:
        self._shadow_buffs(buff_name)
    
    def _remove_redundant_buff(self, buff_dict):
      for buff in self.current_buffs:
        if buff.name == buff_dict['name'] and buff.effect == buff_dict['effect']:
          self.current_buffs.remove(buff)
      self._shadow_buffs(buff_dict['name'])


    # shadows buffs with name, except highest priority buff
    def _shadow_buffs(self, buff_name):
      max_buff_priority = 0
      alive_buff_count = 0
      # find maximum buff priority
      for buff in self.current_buffs:
        if buff.name == buff_name and max_buff_priority < buff.priority:
          max_buff_priority = buff.priority
      # shadow buffs (lower than max_buff_priority)
      for buff in self.current_buffs:
        if buff.name == buff_name:
          if buff.priority < max_buff_priority:
            buff.is_shadowed = True
          else:
            alive_buff_count += 1
      # check alive buff is unique
      if alive_buff_count > 1:
        print('Multiple buff alives after shadowing, check priority of buff dictionary')
        

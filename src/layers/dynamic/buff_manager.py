import importlib
import warnings
from src.layers.dynamic.buff import StatBuff, DamageBuff
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.damage_history import DamageHistory
from src.layers.dynamic.constants import ticks_to_seconds, seconds_to_ticks

class BuffManager():
    def __init__(self, base_character: CharacterLayer, verbose=False, **kwargs):
        self.base_character = base_character
        self.character_specialization = base_character.specialization
        self.verbose = verbose
        self.base_buff_module = importlib.import_module("src.classes.base")
        self.base_buff_table = self.base_buff_module.COMMON_BUFF_DICT
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
            self.register_buff(self.base_buff_module.BASE_BUFF_DICT[buff_name])
        # specialization buff(class specific) is always added
        self.register_buff(self.class_buff_table['Specialization'])
        # add buffs in static_buff_queue, mostly engraving related buffs
        for buff_name in buffs_name_list:
          if buff_name in self.base_buff_table:
            self.register_buff(self.base_buff_table[buff_name])
          elif buff_name in self.class_buff_table:
            self.register_buff(self.class_buff_table[buff_name])
          else:
            warnings.warn(f'Not implemented buff detected, {buff_name}', UserWarning)
    
    def is_buff_exists(self, buff_name):
        for buff in self.current_buffs:
          if buff.name == buff_name:
            return True
        return False
    
    def get_buff(self, buff_name) -> StatBuff | DamageBuff | None:
        if self.is_buff_exists(buff_name):
          for buff in self.current_buffs:
            if buff.name == buff_name:
              return buff
        return None
    
    def apply_function(self, func):
        for buff in self.current_buffs:
          func(buff)

    def register_buff(self, buff_dict, buff_origin: Skill|None=None):
        if self.is_buff_exists(buff_dict['name']):
            buff_name = buff_dict['name']
            if self.verbose:
              print(f'buff already exists, {buff_name} will be shadowed or refreshed')
            if self._try_handle_redundant_buff(buff_dict) == True:
              return
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
            if not buff.buff_type =='stat' or buff.is_shadowed or buff.effect is None:
                continue
            # get buff's effect and apply to character and skill
            buff_effect = self._get_buff_effect(buff)
            buff_effect(character, skill, buff)
        skill.set_buff_applied()
    
    def calc_damage_from_buffs(self, damage_history: DamageHistory, skill_manager: SkillManager):
        for buff in self.current_buffs:
          if buff.buff_type == 'damage':
            character = self.base_character.copy()
            dummy_skill = skill_manager.dummy_skill.copy()
            is_awakening = False
            if buff.buff_origin is not None:
              dummy_skill.identity_type = buff.buff_origin.identity_type
              is_awakening = bool(dummy_skill.identity_type == 'Awakening')
            self.apply_stat_buffs(character, dummy_skill)
            damage = buff.calc_damage(character, dummy_skill, self.current_tick)
            if damage > 0:
              if self.verbose:
                print(f'{buff.name} dealt {damage} on {ticks_to_seconds(self.current_tick)}s')
              damage_history.register_damage(f"{buff.name}|{buff.buff_origin}", damage, 0, is_awakening, self.current_tick)

    def print_buffs(self):
        print(self.current_buffs)
    
    def _get_buff_effect(self, buff: StatBuff):
        buff_body = getattr(self.base_buff_module, buff.effect, None)
        if buff_body is None:
          buff_body = getattr(self.class_buff_module, buff.effect)
        return buff_body
    
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
    
    # if buff is identical to target buff, extend duration
    def _try_handle_redundant_buff(self, buff_dict):
      for buff in self.current_buffs:
        if buff.name == buff_dict['name'] and buff.effect == buff_dict['effect']:
          new_duration = (self.current_tick - buff.begin_tick) + seconds_to_ticks(buff_dict['duration'])
          buff.duration = max(buff.duration, new_duration)
          return True
      return False

    # if buff has same name but different effect, check priority and use hightest one only
    # buffs that are not used are marked with shadowed flag (is_shadowed as True) 
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
        print('Multiple buff alive after shadowing, check priority of buff dictionary')
        

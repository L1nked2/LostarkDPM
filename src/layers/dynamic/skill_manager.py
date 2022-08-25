
import importlib
import json
import warnings
from collections import deque
from src.layers.static.character_layer import CharacterLayer
from .skill import Skill
from .constants import seconds_to_ticks

DEFAULT_LOOKUP_COOLDOWN = 5

class SkillManager:

    def __init__(self, character: CharacterLayer, **kwargs):
        skill_info = json.load(open(character.skill_set, "r", encoding='utf-8'))
        class_name = skill_info['class_name']
        if character.class_name != class_name:
            warnings.warn("Class of character and skill_set does not match", UserWarning)
        self.last_tick = 0
        self.blocked_until = -1
        # import policy
        self._import_policy(skill_info['policy'])
        # import skills
        self.skill_pool = dict()
        for naive_skill in skill_info['skill_preset']:
            self.skill_pool[naive_skill['name']] = Skill(**naive_skill)
        self._validate_jewel()
        # finalize skill(tripod)
        import_target = "src.classes." + class_name
        class_module = importlib.import_module(import_target)
        if hasattr(class_module, 'finalize_skill'):
          for skill_name in self.skill_pool:
            class_module.finalize_skill(self.skill_pool[skill_name])
        # dummy skill
        self.dummy_skill = Skill('dummy', 0, None, None, 0, 0, 0, False, False)
        # 룬 통계
        self.rune_ratio = {'rg': [0,0], 'qr': [0,0], 'jm' : [0,0]}

        print('##### Done Initialization of SkillsManager #####')
    
    def update_tick(self, current_tick):
        tick_diff = current_tick - self.last_tick
        cooldown_func = lambda x: x - tick_diff
        for skill_name in self.skill_pool:
          self.skill_pool[skill_name].update_remaining_cooldown(cooldown_func)
        # update block status
        if self.blocked_until < current_tick:
          self.is_blocked = False
        else:
          self.is_blocked = True
        self.last_tick = current_tick
    
    def apply_function(self, func):
        for skill_name in self.skill_pool:
          func(self.skill_pool[skill_name])

    def block_until(self, tick):
        self.blocked_until = tick
    
    def is_next_cycle_available(self):
      # (is character available, is next skill available)
      # True, True -> use_skill
      # True, False -> idle
      # False, T/F -> blocked
      self._fetch_next_skills()
      if len(self.skill_queue) == 0:
        return (not self.is_blocked, False)
      target_name = self.skill_queue[0]
      return (not self.is_blocked, bool(self.skill_pool[target_name].remaining_cooldown <= 0))

    def get_next_skill(self) -> Skill:
        self._fetch_next_skills()
        target_name = self.skill_queue.popleft()
        return self.skill_pool[target_name]
    
    def print_skills(self):
        skills = list(self.skill_pool.items())
        print('Skills: (', end='')
        for skill in skills[:-1]:
            print(skill[0], end=', ')
        print(skills[-1][0], end='')
        print(')')

    def _import_policy(self, policy_contents):
        self.policy = dict()
        self.mode = policy_contents['mode']
        if not self.mode in ['scheduler', 'fixed']:
            warnings.warn("Invalid mode given", UserWarning)
        if self.mode == 'scheduler':
            scheduler_parameters = ['priorities', 'bindings','lookup_cooldown']
            default_values = [dict(), dict(), DEFAULT_LOOKUP_COOLDOWN]
            for variable in scheduler_parameters:
              if variable in policy_contents:
                self.policy[variable] = policy_contents[variable]
              else:
                self.policy[variable] = default_values[variable]
        elif self.mode == 'fixed':
            scheduler_parameters = ['main_cycle']
            default_values = [list()]
            for variable in scheduler_parameters:
              if variable in policy_contents:
                self.policy[variable] = policy_contents[variable]
              else:
                self.policy[variable] = default_values[variable]
        self.skill_queue = deque()

    def _validate_jewel(self):
        jewel_count = 0
        for skill_name in self.skill_pool:
            if self.skill_pool[skill_name].jewel_cooldown_level > 0:
                jewel_count += 1
            if self.skill_pool[skill_name].jewel_damage_level > 0:
                jewel_count += 1
        if jewel_count > 11:
            print(f"Too many jewels, {jewel_count} > 11")
        elif jewel_count < 11:
            print(f"Not enough jewels, {jewel_count} < 11")
        
    """def _is_awakening_skill_available(self):
        for skill_name in self.skill_pool:
          if self.skill_pool[skill_name].identity_type == 'Awakening':
            return bool(self.skill_pool[skill_name].remaining_cooldown <= 0)
        return False"""
    
    def _is_skill_available(self, target_skill_name):
        return self._is_skill_available_on(target_skill_name, self.last_tick)
    
    def _is_skill_available_on(self, target_skill_name, target_tick):
        tick_diff = target_tick - self.last_tick
        for skill_name in self.skill_pool:
            if self.skill_pool[skill_name].name == target_skill_name:
              return bool(self.skill_pool[skill_name].remaining_cooldown <= tick_diff)
        return False
    
    def _fetch_next_skills(self):
        if self.mode == 'scheduler':
          # TODO
          print('scheduler is not implemented yet')
          pass
        elif self.mode == 'fixed':
          if len(self.skill_queue) == 0:
            self.skill_queue = deque(self._select_cycle())
        else:
          raise Exception('Not implemented skill manager mode')
    
    def _select_cycle(self):
        cycle_index = -1
        for cycle in self.policy['main_cycle']:
          cycle_available = self._estimate_cycle_availablility(cycle)
          if cycle_available:
            cycle_index = self.policy['main_cycle'].index(cycle)
            break
        if cycle_index < 0:
          return list()
        else:
          return self.policy['main_cycle'][cycle_index]

    def _estimate_cycle_availablility(self, cycle):
        tick = self.last_tick
        for skill_name in cycle:
          if not self._is_skill_available_on(skill_name, tick):
            return False
          tick += self.skill_pool[skill_name].prev_delay
        return True
    
    def _block_awakening_skill(self):
        for skill_name in self.skill_pool:
          if self.skill_pool[skill_name].identity_type == 'Awakening':
            return bool(self.skill_pool[skill_name].remaining_cooldown <= 0)
        return False

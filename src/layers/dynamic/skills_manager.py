
import importlib
import json
import warnings
import queue
from collections import deque
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill
DEFAULT_LOOKUP_COOLDOWN = 5

class SkillsManager:

    def __init__(self, character: CharacterLayer, **kwargs):
        skill_info = json.load(open(character.skill_set, "r", encoding='utf-8'))
        class_name = skill_info['class_name']
        if character.class_name != class_name:
            warnings.warn("Class of character and skill_set does not match", UserWarning)
        self.last_tick = 0
        #TODO: import identity
        # import policy
        self._import_policy(skill_info['policy'])
        # import skills
        self.skill_pool = dict()
        for naive_skill in skill_info['skill_preset']:
            self.skill_pool[naive_skill['name']] = Skill(**naive_skill)
        self._validate_jewel()

        print('##### Done Initialization of SkillsManager #####')

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
            self.skill_queue = queue.PriorityQueue()
        elif self.mode == 'fixed':
            scheduler_parameters = ['main_cycle', 'awakening_cycle']
            default_values = [list()]
            for variable in scheduler_parameters:
              if variable in policy_contents:
                self.policy[variable] = policy_contents[variable]
              else:
                self.policy[variable] = default_values[variable]
            self.skill_queue = deque(self.policy['awakening_cycle'])

    def _validate_jewel(self):
        jewel_count = 0
        for skill_name in self.skill_pool:
            if self.skill_pool[skill_name].jewel_cooldown_level > 0:
                jewel_count += 1
            if self.skill_pool[skill_name].jewel_damage_level > 0:
                jewel_count += 1
        if jewel_count > 11:
            warnings.warn(f"Too many jewels, {jewel_count} > 11", UserWarning)
        elif jewel_count < 11:
            warnings.warn(f"Not enough jewels, {jewel_count} < 11", UserWarning)
    
    def update_tick(self, current_tick):
        tick_diff = current_tick - self.last_tick
        cooldown_func = lambda x: x - tick_diff
        for skill_name in self.skill_pool:
          self.skill_pool[skill_name].update_remaining_cooldown(cooldown_func)
        self.last_tick = current_tick
    
    def apply_function(self, func):
        for skill_name in self.skill_pool:
          func(self.skill_pool[skill_name])

    def get_next_skill(self) -> Skill:
        if self.mode == 'scheduler':
          # TODO
          print('scheduler is not implemented yet')
          pass
        elif self.mode == 'fixed':
          if len(self.skill_queue) == 0:
            if self.is_awakening_skill_available() == True:
              self.skill_queue.extend(self.policy['awakening_cycle'])
            else:
              self.skill_queue.extend(self.policy['main_cycle'])
          target_name = self.skill_queue.popleft()
          return self.skill_pool[target_name]

    def is_awakening_skill_available(self):
        for skill_name in self.skill_pool:
          if self.skill_pool[skill_name].identity_type == 'Awakening':
            return bool(self.skill_pool[skill_name].remaining_cooldown == 0)
        return False

    def print_skills(self):
        skills = list(self.skill_pool.items())
        print('Skills: (', end='')
        for skill in skills[:-1]:
            print(skill[0], end=', ')
        print(skills[-1][0], end='')
        print(')')

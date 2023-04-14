"""
Basic skill class

data example
{
  "name": "버스트 캐넌",
  "default_damage": 3075,
  "tripod": "312",
  "level": 12,
  "default_coefficient": 19.06, -> optional
  "base_damage_multiplier": 6.0512,
  "skill_type": "Charge",
  "identity_type": "Lance",
  "cooldown": 30,
  "common_delay": 1.0,
  "type_specific_delay": 1.0,
  "jewel_cooldown_level": 7,
  "jewel_damage_level": 7,
  "head_attack": true,
  "back_attack": false,
  'base_additional_crit_rate': 0.0, -> optional
  'base_additional_crit_damage': 0.0, -> optional
  "triggered_actions": [], -> optional
  "key_strokes" : 1,
  'mana_cost': 1, -> optional
  "rune": "질풍_영웅"
}
"""
import copy
import warnings
import src.layers.dynamic.constants as constants
from src.layers.core.utils import seconds_to_ticks
from ..core.utils import ResourcePacker
from ..core.skill_base import SkillBase
from .common_term import *

DEFAULT_PRIORITY = 10
SKILL_TYPES = ['Common', 'Combo', 'Chain', 'Point', 'Holding_A', 'Holding_B', 'Casting', 'Charge']


class Skill(SkillBase):
    def __init__(self, class_name, name, default_damage=0,
                  skill_type=None, identity_type=None, cooldown=0,
                  common_delay=0, type_specific_delay=0,
                  head_attack=False, back_attack=False,
                  level=12, default_coefficient=0, 
                  triggered_actions=None, **kwargs):
        terms = [CommonTerm.base_damage_term(), CommonTerm.crit_term(), CommonTerm.defense_term(), CommonTerm.total_multiplier_term()]
        super().__init__(name, class_name, default_damage, default_coefficient, cooldown, triggered_actions, terms, **kwargs)
        self.level = level
        if default_coefficient <= 0:
          self._default_coefficient = self.default_damage * constants.SKILL_DAMAGE_COEFF[class_name][level]
        self.skill_type = skill_type
        self.identity_type = identity_type
        self.base_common_delay = seconds_to_ticks(common_delay)
        self.base_type_specific_delay = seconds_to_ticks(type_specific_delay)
        self.head_attack = head_attack
        self.back_attack = back_attack
        if self.identity_type == 'Awakening':
          self.triggered_actions += ['try_activate_dominion_set']

        # handle additional variables
        # default values
        self.tripod = '000'
        self.base_damage_multiplier = 1.0
        self.jewel_cooldown_level = 0
        self.jewel_damage_level = 0
        self.cooldown_on_finish = False
        self.base_additional_crit_rate = 0.0
        self.base_additional_crit_damage = 0.0
        self.base_defense_reduction_rate = 0.0
        self.key_strokes = 0
        self.rune = None
        self.mana_cost = 1
        self._set_additional_variables(**kwargs)
        self._apply_jewel()
        self._apply_rune()
        
        # reset variables
        self.reset()
        # validation
        self._validate_skill()
        

        # delay estimation
        self.prev_delay = self.actual_delay
    
    # hardcopy method
    def copy(self):
        return copy.deepcopy(self)
    
    # cancel buffs
    def reset(self):
        super().reset()
        self.common_delay = self.base_common_delay
        self.type_specific_delay = self.base_type_specific_delay
        self.damage_multiplier = self.base_damage_multiplier
        self.crit_rate = self.base_additional_crit_rate
        self.crit_damage = self.base_additional_crit_damage
        self.defense_reduction_rate = self.base_defense_reduction_rate
        self._refresh_skill()

    def _set_additional_variables(self, **kwargs):
        additional_variables = [
          'tripod',
          'base_damage_multiplier',
          'jewel_cooldown_level',
          'jewel_damage_level',
          'cooldown_on_finish',
          'key_strokes',
          'base_additional_crit_rate',
          'base_additional_crit_damage',
          'base_defense_reduction_rate',
          'rune',
          'mana_cost',
        ]
        for variable in additional_variables:
          if variable in kwargs:
            self.__setattr__(variable, kwargs[variable])

        # cooldown_on_finish
        cooldown_on_finish_types = ['Chain', 'Casting', 'Holding_B']
        if self.skill_type in cooldown_on_finish_types:
            self.cooldown_on_finish = True
        # rune parsing
        if self.rune == 'None':
          self.rune = None
        if self.rune:
          self.rune_level = self.rune[3:]
          self.rune = self.rune[:2]
    
    def _validate_skill(self):
        super()._validate_skill()
        if not (self.skill_type in SKILL_TYPES or self.skill_type is None):
            warnings.warn(f"invalid skill type given, {self.skill_type}", UserWarning)
        if self.base_common_delay < 0 or self.base_type_specific_delay < 0:
            warnings.warn("Delay cannot be negative", UserWarning)
        if self.jewel_cooldown_level < 0 or self.jewel_damage_level < 0:
            warnings.warn("Jewel level cannot be negative", UserWarning)
        #TODO: check skill identity_type is in predefined identity types in specific class.py
    
    def _is_skill_available(self):
        return super()._is_skill_available()
        
    def _refresh_skill(self):
        self.actual_delay = self.common_delay + self.type_specific_delay

    # Get method
    def get_attribute(self, target):
        try:
            result = getattr(self, target)
        except AttributeError as e:
            print(e)
        else:
            return result

    # Update method
    def update_attribute(self, target, new_value):
        try:
            getattr(self, target)
        except AttributeError as e:
            print(e)
        else:
            setattr(self, target, new_value)
        self._refresh_skill()

    def _apply_jewel(self):
        cj = constants.COOLDOWN_JEWEL_LIST[self.jewel_cooldown_level]
        dj = constants.DAMAGE_JEWEL_LIST[self.jewel_damage_level]
        self._base_cooldown = self._base_cooldown * (1 - cj)
        self.base_damage_multiplier = self.base_damage_multiplier * (1 + dj)
    
    def _apply_rune(self):
        if self.rune:
          if self.rune == '질풍':
            additional_attack_speed = constants.get_rune_effect(self.rune, self.rune_level)
            self.base_common_delay = self.base_common_delay / (1 + additional_attack_speed)
            self.base_type_specific_delay = (self.base_type_specific_delay / 
                                              (1 + additional_attack_speed))
          else:
            effect = constants.get_rune_effect(self.rune, self.rune_level)
            if effect is not None:
              self._triggered_actions.append(effect)

    def start_cooldown(self, cooldown_reduction):
        if self.cooldown_on_finish:
          if self.skill_type == 'Chain':
            self._remaining_cooldown = self._actual_cooldown * (1-cooldown_reduction) + self.common_delay
          else:
            self._remaining_cooldown = self._actual_cooldown * (1-cooldown_reduction) + self.actual_delay
        else:
            self._remaining_cooldown = self._actual_cooldown * (1-cooldown_reduction)
    
    def update_remaining_cooldown(self, function):
        self._remaining_cooldown = max(0, function(self._remaining_cooldown))
    
    def calc_damage(self, res_pack:ResourcePacker):
        damage = super().calc_damage(res_pack)
        return damage
    
    def calc_delay(self, attack_speed):
        self.common_delay = self.common_delay / attack_speed
        self.type_specific_delay = self.type_specific_delay / attack_speed
        self._refresh_skill()
        delay = self.actual_delay
        self.prev_delay = delay
        return delay

    def __repr__(self):
        info = f'{self.name}'
        return info

    def print_skill_info(self):
        targets = ['name', 'default_damage', 'default_coefficient', 'damage_multiplier', 'additional_crit_rate', 'additional_crit_damage', 'actual_delay']
        for target in targets:
            print(f'{target}: {self.__getattribute__(target)}')

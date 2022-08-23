"""
Basic skill class

data example
{
  "name": "버스트 캐넌",
  "default_damage": 3075,
  "default_coefficient": 19.06,
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
  "triggered_actions": [],
  "key_strokes" : 1,
  "rune": "질풍_영웅"
}
"""
import copy
import warnings
import src.layers.dynamic.constants as constants
from src.layers.utils import crit_to_multiplier

DEFAULT_PRIORITY = 10
SKILL_TYPES = ['Common', 'Combo', 'Chain', 'Point', 'Holding_A', 'Holding_B', 'Casting', 'Charge']

class Skill:
    def __init__(self, name, default_damage, default_coefficient, 
                  skill_type, identity_type, cooldown,
                  common_delay, type_specific_delay,
                  head_attack, back_attack,
                  triggered_actions=list(), **kwargs):
        self.name = name
        self.default_damage = default_damage
        self.default_coefficient = default_coefficient
        self.base_cooldown = constants.seconds_to_ticks(cooldown)
        self.skill_type = skill_type
        self.identity_type = identity_type
        self.base_common_delay = constants.seconds_to_ticks(common_delay)
        self.base_type_specific_delay = constants.seconds_to_ticks(type_specific_delay)
        self.head_attack = head_attack
        self.back_attack = back_attack
        self.triggered_actions = ['default_action'] + triggered_actions
        if self.identity_type == 'Awakening':
          self.triggered_actions += ['activate_dominion_set']

        # handle additional variables
        self._init_additional_variables(**kwargs)
        self._apply_jewel()
        self._apply_rune()
        if self.skill_type == 'Chain':
          for i in range(self.key_strokes-1):
            self.triggered_actions.extend(self.triggered_actions)

        # simulation variables
        self.actual_cooldown = self.base_cooldown
        self.remaining_cooldown = 0.0
        self.priority = DEFAULT_PRIORITY

        # validation
        self._validate_skill()

        # reset variables
        self.reset()

        # delay estimation
        self.prev_delay = self.actual_delay
    
    def copy(self):
        return copy.deepcopy(self)
    
    # cancel buffs
    def reset(self):
        self.buff_applied = False
        self.actual_cooldown = self.base_cooldown
        self.common_delay = self.base_common_delay
        self.type_specific_delay = self.base_type_specific_delay
        self.damage_multiplier = self.base_damage_multiplier
        self.additional_crit_rate = self.base_additional_crit_rate
        self.additional_crit_damage = self.base_additional_crit_damage
        self._refresh_skill()

    def _init_additional_variables(self, **kwargs):
        default_values = {
          'tripod': '000',
          'base_damage_multiplier': 1.0,
          'jewel_cooldown_level': 0,
          'jewel_damage_level': 0,
          'cooldown_on_finish': False,
          'key_strokes': 0,
          'base_additional_crit_rate': 0.0,
          'base_additional_crit_damage': 0.0,
          'rune': None,
          'mana_cost': 1,
        }
        for variable in default_values:
          if variable in kwargs:
            self.__setattr__(variable, kwargs[variable])
          else:
            self.__setattr__(variable, default_values[variable])

        # cooldown_on_finish
        cooldown_on_finish_types = ['Combo', 'Chain', 'Casting', 'Holding_B']
        if self.skill_type in cooldown_on_finish_types:
            self.cooldown_on_finish = True
        # rune parsing
        if self.rune == 'None':
          self.rune = None
        if self.rune:
          self.rune_level = self.rune[3:]
          self.rune = self.rune[:2]
    
    def _validate_skill(self):
        if self.default_damage < 0 or self.default_coefficient < 0:
            warnings.warn("Damage and coefficient cannot be negative", UserWarning)
        if not (self.skill_type in SKILL_TYPES or self.skill_type is None):
            warnings.warn(f"invalid skill type given, {self.skill_type}", UserWarning)
        if self.base_common_delay < 0 or self.base_type_specific_delay < 0:
            warnings.warn("Delay cannot be negative", UserWarning)
        if self.jewel_cooldown_level < 0 or self.jewel_damage_level < 0:
            warnings.warn("Jewel level cannot be negative", UserWarning)
        
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
        self.base_cooldown = self.base_cooldown * (1 - cj)
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
              self.triggered_actions.append(effect)

    def update_priority(self, new_priority):
        self.priority = new_priority

    def start_cooldown(self, cooldown_reduction):
        if self.cooldown_on_finish:
          if self.skill_type == 'Combo':
            self.remaining_cooldown = self.actual_cooldown * (1-cooldown_reduction) + self.common_delay
          else:
            self.remaining_cooldown = self.actual_cooldown * (1-cooldown_reduction) + self.actual_delay
        else:
            self.remaining_cooldown = self.actual_cooldown * (1-cooldown_reduction)
    
    def update_remaining_cooldown(self, function):
        self.remaining_cooldown = max(0, function(self.remaining_cooldown))

    def calc_damage(self, attack_power, crit_rate, crit_damage, total_multiplier):
        if not self.remaining_cooldown <= 0:
          warnings.warn(f"Damage calculation before cooldown finished, check skill {self.name}", UserWarning)
        if not self.buff_applied:
          warnings.warn("Damage calculation before buff applied", UserWarning)
        crit_multiplier = crit_to_multiplier(crit_rate + self.additional_crit_rate, crit_damage + self.additional_crit_damage)
        damage = ((self.default_damage + attack_power * self.default_coefficient)
                   * self.damage_multiplier * crit_multiplier * total_multiplier)
        return damage
    
    def calc_delay(self, attack_speed):
        delay = self.actual_delay / attack_speed
        self.prev_delay = delay
        return delay

    def __repr__(self):
        info = f'{self.name}'
        return info

    def print_skill_info(self):
        targets = ['name', 'damage_multiplier', 'additional_crit_rate', 'additional_crit_damage', 'actual_delay']
        for target in targets:
            print(f'{target}: {self.__getattribute__(target)}')

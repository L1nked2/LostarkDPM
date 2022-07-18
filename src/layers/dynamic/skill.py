"""
Basic skill class

data example
{
  "name": "배쉬",
  "default_damage": 2997,
  "default_coefficient": 18.593,
  "skill_type": "Common",
  "identity_type": "Common",
  "common_delay": 1.0,
  "type_specific_delay": 0,
  "jewel_cooldown_level": 7,
  "jewel_damage_level": 7,
  "head_attack": true,
  "back_attack": false,
  "triggered_actions": ["AP_buff_1"],
  "key_strokes" : 1
}
"""
import warnings
import src.layers.dynamic.constants as constants
from src.layers.utils import crit_to_multiplier

class Skill:
    def __init__(self, name, default_damage, default_coefficient, 
                  skill_type, identity_type, cooldown,
                  common_delay, type_specific_delay,
                  head_attack, back_attack,
                  triggered_actions, **kwargs):
        self.name = name
        self.default_damage = default_damage
        self.default_coefficient = default_coefficient
        self.cooldown = constants.seconds_to_ticks(cooldown)
        self.skill_type = skill_type
        self.identity_type = identity_type
        self.common_delay = common_delay
        self.type_specific_delay = type_specific_delay
        self.head_attack = head_attack
        self.back_attack = back_attack
        self.triggered_actions = triggered_actions

        # handle additional variables
        self._handle_additional_variables(**kwargs)

        # simulation variables
        self.base_damage_multiplier = 1.0
        self.remaining_cooldown = 0
        self.priority = 10
        self.apply_jewel()

        # reset variables
        self.reset_simulation_variables()

    def _handle_additional_variables(self, **kwargs):
        default_values = {
          'jewel_cooldown_level': 0,
          'jewel_damage_level': 0,
          'cooldown_on_finish': False,
          'key_strokes': 0,
          'base_additional_crit_rate': 0.0,
          'base_additional_crit_damage': 0.0,
        }
        for variable in default_values:
          if variable in kwargs:
            self.__setattr__(variable, kwargs[variable])
          else:
            self.__setattr__(variable, default_values[variable])

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

    def apply_jewel(self):
        cj = constants.COOLDOWN_JEWEL_LIST[self.jewel_cooldown_level]
        dj = constants.DAMAGE_JEWEL_LIST[self.jewel_damage_level]
        self.cooldown = self.cooldown * (1 - cj)
        self.base_damage_multiplier = self.base_damage_multiplier * (1 + dj)

    def reset_simulation_variables(self):
        self.buff_applied = False
        self.damage_multiplier = self.base_damage_multiplier
        self.additional_crit_rate = self.base_additional_crit_rate
        self.additional_crit_damage = self.base_additional_crit_damage
        self.actual_delay = self.common_delay + self.type_specific_delay
    
    def tick(self):
        self.remaining_cooldown -= 1

    def start_cooldown(self, cooldown_reduction):
        self.remaining_cooldown = self.cooldown * (1-cooldown_reduction)
    
    def update_priority(self, new_priority):
        self.priority = new_priority
    
    def update_remaining_cooldown(self, new_cooldown):
        self.remaining_cooldown = new_cooldown

    def calc_damage(self, actual_attack_power, crit_rate, crit_damage, total_multiplier):
        if not self.buff_applied:
          warnings.warn("Damage calculation before buff applied", UserWarning)
        crit_multiplier = crit_to_multiplier(crit_rate + self.additional_crit_rate, crit_damage + self.additional_crit_damage)
        damage = ((self.default_damage + actual_attack_power) * self.default_coefficient 
                   * self.damage_multiplier * crit_multiplier * total_multiplier)
        return damage

    def __repr__(self):
        info = f'{self.name}'
        return info

    def print_skill_info(self):
        print(f"Name: {self.name}")

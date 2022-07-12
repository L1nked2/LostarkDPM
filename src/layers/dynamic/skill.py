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
  "triggered_actions": ["AP_buff_1"]
}
"""
import warnings
import src.layers.dynamic.constants as constants

class Skill:
    def __init__(self, name, default_damage, default_coefficient, 
                  skill_type, identity_type, cooldown,
                  common_delay, type_specific_delay,
                  jewel_cooldown_level, jewel_damage_level,
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
        self.jewel_cooldown_level = jewel_cooldown_level
        self.jewel_damage_level = jewel_damage_level
        self.head_attack = head_attack
        self.back_attack = back_attack
        self.triggered_actions = triggered_actions

        # simulation variables
        self.base_damage_multiplier = 1.0
        self.remaining_cooldown = 0
        self.priority = 10
        self.apply_jewel()

        # reset variables
        self.reset_simulation_variables()

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
        self.additional_crit_rate = 0.0
        self.actual_delay = self.common_delay + self.type_specific_delay
    
    def tick(self):
        self.remaining_cooldown -= 1
    
    def update_priority(self, new_priority):
        self.priority = new_priority
    
    def update_remaining_cooldown(self, new_cooldown):
        self.remaining_cooldown = new_cooldown

    def calc_damage(self, actual_attack_power):
        if not self.buff_applied:
          warnings.warn("Damage calculation before buff applied", UserWarning)
        damage = (self.default_damage + actual_attack_power) * self.default_coefficient * self.damage_multiplier
        return damage

    def print_skill_info(self):
        print(f"Name: {self.data['name']}")

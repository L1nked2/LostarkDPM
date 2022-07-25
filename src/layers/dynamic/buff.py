"""
Basic buff classes
"""
from src.layers.dynamic.constants import *

MAX_PRIORITY = 31

class Buff:
    """Base class for buff"""
    def __init__(self, name, buff_type, buff_origin, effect, duration, priority, begin_tick):
        self.name = name
        self.buff_type = buff_type
        self.buff_origin = buff_origin
        self.effect = effect
        self.duration = seconds_to_ticks(duration)
        self.priority = priority
        self.begin_tick = begin_tick
        self.is_shadowed = False

    def is_expired(self, current_tick) -> bool:
        return self.begin_tick + self.duration <= current_tick
        
    def __repr__(self):
        return str({'name': self.name, 'begin_tick': self.begin_tick, 'duration': ticks_to_seconds(self.duration), 'is_shadowed': self.is_shadowed})

class StatBuff(Buff):
    """Class for stat buff"""
    def __init__(self, **kwargs):
        super(StatBuff, self).__init__(**kwargs)

class DamageBuff(Buff):
    """Class for Damage buff"""
    def __init__(self, base_damage, coefficient, **kwargs):
        super(DamageBuff, self).__init__(**kwargs)
        self.base_damage = base_damage
        self.coefficient = coefficient
    
    def apply_damage_buff(self, character, current_tick) -> int:
        damage_value = 0
        #last visited tick?
        if (current_tick - self.start_tick) % TICKS_PER_SECOND == 0:
          damage_value = (self.base_damage + (self.coefficient * character.actual_attack_power)) * character.total_multiplier
        return damage_value

        



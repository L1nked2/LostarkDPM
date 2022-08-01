"""
Basic buff classes
"""
from src.layers.dynamic.constants import *
from src.layers.utils import crit_to_multiplier

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
        self.stack = 0

    def is_expired(self, current_tick) -> bool:
        return self.begin_tick + self.duration < current_tick
    
    def increase_stack(self):
        self.stack += 1
        
    def __repr__(self):
        return str({'name': self.name, 'begin_tick': self.begin_tick, 'duration': ticks_to_seconds(self.duration), 'is_shadowed': self.is_shadowed})

class StatBuff(Buff):
    """Class for stat buff"""
    def __init__(self, **kwargs):
        super(StatBuff, self).__init__(**kwargs)

class DamageBuff(Buff):
    """Class for Damage buff"""
    def __init__(self, base_damage, coefficient, damage_interval, **kwargs):
        super(DamageBuff, self).__init__(**kwargs)
        self.base_damage = base_damage
        self.coefficient = coefficient
        self.last_tick = self.begin_tick
        self.damage_interval = seconds_to_ticks(damage_interval)
    
    #TODO:is shadowd needed
    def calc_damage_buff(self, attack_power, crit_rate, crit_damage, total_multiplier, current_tick) -> int:
        damage_value = 0
        tick_diff = current_tick - self.last_tick
        crit_multiplier = crit_to_multiplier(crit_rate, crit_damage)
        if tick_diff >= self.damage_interval:
          damage_value = (tick_diff // self.damage_interval) * (self.base_damage + attack_power) * self.coefficient * crit_multiplier * total_multiplier
          self.last_tick = current_tick
        return round(damage_value)

        



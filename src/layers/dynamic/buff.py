"""
Basic buff classes
StatBuff, SkillBuff. DamageBuff inherits Buff
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.constants import *

class Buff:
    """Base class for buff"""
    def __init__(self, name, buff_type, sources, target, effect, duration, priority, begin_tick):
        self.name = name
        self.buff_type = buff_type
        self.sources = sources
        self.target = target
        self.effect = effect
        self.duration = duration
        self.priority = priority
        self.begin_tick = begin_tick

    def is_expired(self, current_tick) -> bool:
        return self.begin_tick + self.duration <= current_tick
    
    def __repr__(self):
        return str({'name': self.name, 'begin_tick': self.begin_tick, 'duration': self.duration})

class StatBuff(Buff):
    """Class for stat buff"""
    def __init__(self, **kwargs):
        super(StatBuff, self).__init__(**kwargs)
    
    def apply_stat_buff(self, character: CharacterLayer) -> CharacterLayer:
        source_value = tuple()
        for attr in self.sources:
          source_value += character.get_attribute(attr)
        result = self.effect(source_value)
        print(f'buff test: ', result) ###test
        character.update_attribute(self.target, result)

class SkillBuff(Buff):
    """Class for skill buff"""
    def __init__(self, **kwargs):
        super(SkillBuff, self).__init__(**kwargs)
    
    def apply_skill_buff(self, skill: Skill) -> Skill:
        pass

class DamageBuff(Buff):
    """Class for Damage buff"""
    def __init__(self, base_damage, coefficient, **kwargs):
        super(DamageBuff, self).__init__(**kwargs)
        self.base_damage = base_damage
        self.coefficient = coefficient
    
    def apply_damage_buff(self, character: CharacterLayer, current_tick) -> int:
        damage_value = 0
        #last visited tick?
        if (current_tick - self.start_tick) % TICKS_PER_SECOND == 0:
          damage_value = (self.base_damage + (self.coefficient * character.actual_attack_power)) * character.total_multiplier
        return damage_value

        



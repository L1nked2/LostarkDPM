from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.constants import *

class Buff:
    """Base class for buff"""
    def __init__(self, name, expires_at):
        self.name = name
        self.expires_at = expires_at

    def is_expired(self, current_tick) -> bool:
        return self.expires_at >= current_tick

class StatBuff(Buff):
    """Class for stat buff"""
    def __init__(self, effects, **kwargs):
        super(StatBuff, self).__init__(**kwargs)
        self.effects = effects
        # lambda functions, takes target and source to modify target
        # ex) [(target, source, lambda x,y: x + y)]
    
    def apply_stat_buff(self, character: CharacterLayer) -> CharacterLayer:
        for effect in self.effects:
          target = getattr(character, effect[0])
          source = getattr(character, effect[1])
          result = getattr(character, effect[2])(target, source)
          setattr(character, target, result)

class SkillBuff:
    """Class for skill buff"""
    def __init__(self, conditions, effects, **kwargs):
        super(StatBuff, self).__init__(**kwargs)
        self.conditions = conditions
        # lambda functions, takes target return bool
        # ex) [(target, lambda x: True if x == 'back' else False)]
        self.effects = effects
        if len(conditions) != len(effects):
          print('length of conditions must be equal to length of effects')
          raise ValueError
    
    def apply_skill_buff(self, skill: Skill) -> Skill:
        effect_bool = list()
        for condition in self.conditions:
          target = getattr(skill.attributes, condition)
        for effect in zip(effect_bool, self.effects):
          pass #TODO: fill this after skill is finished

class DamageBuff:
    """Class for Damage buff"""
    def __init__(self, base_damage, coefficient, start_tick, total_tick, **kwargs):
        super(StatBuff, self).__init__(**kwargs)
        self.base_damage = base_damage
        self.coefficient = coefficient
        self.start_tick = start_tick
        self.total_tick = total_tick
    
    def apply_damage_buff(self, character: CharacterLayer, current_tick) -> int:
        damage_value = 0
        if (current_tick - self.start_tick) % TICKS_PER_SECOND == 0:
          damage_value = (self.base_damage + (self.coefficient * character.actual_attack_power)) * character.total_multiplier
        return damage_value

        



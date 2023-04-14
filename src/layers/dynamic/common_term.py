"""
Pre-defined terms to plugin
"""
import warnings
from ..core.term_base import TermBase
from ..static.constants import DEFAULT_DEFENSE, DEFENSE_CORRECTION


"""
Base damage generator
"""
def base_damage_term(default_damage, attack_power, default_coefficient, damage_multiplier):
  if default_damage < 0 or attack_power < 0 or default_coefficient < 0:
    warnings.warn("Default damage, attack power, default coefficient must be positive")
    return 0
  return (default_damage + attack_power * default_coefficient) * damage_multiplier
"""
Crit stats to multiplier helper
"""
def crit_to_multiplier(crit_rate, crit_damage):
  if crit_rate < 0 or crit_damage < 0:
    warnings.warn("Crit rate and crit damage must be positive")
    crit_rate = 0
    crit_damage = 0
  crit_rate = min(crit_rate, 1.0)
  return crit_rate * crit_damage + (1 - crit_rate) * 1.0

"""
Defense reduction rate to multiplier helper
"""
def defense_reduction_to_multiplier(defense_reduction_rate):
  if defense_reduction_rate < 0:
    warnings.warn("Defense reduction rate must be positive")
    defense_reduction_rate = 0
  defense_reduction_rate = min(defense_reduction_rate, 1.0)
  return DEFAULT_DEFENSE / (DEFAULT_DEFENSE * (1.0 - defense_reduction_rate) + DEFAULT_DEFENSE) * DEFENSE_CORRECTION

"""
Terms derived from TermBase
"""
class CommonTerm(TermBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    @classmethod
    def base_damage_term(cls):
        return cls('Base_Damage_Term', ['default_damage', 'actual_attack_power', 'default_coefficient', 'damage_multiplier'], base_damage_term)
    
    @classmethod
    def crit_term(cls):
        return cls('Crit_Term', ['crit_rate', 'crit_damage'], crit_to_multiplier)

    @classmethod
    def defense_term(cls):
        return cls('Defense_Term', ['defense_reduction_rate'], defense_reduction_to_multiplier)
    
    @classmethod
    def total_multiplier_term(cls):
        return cls('Total_Multiplier_Term', ['total_multiplier'], lambda x: x)



    




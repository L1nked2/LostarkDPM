"""
Basic skill class
"""

import copy
import warnings
from .utils import seconds_to_ticks, ticks_to_seconds
#from src.layers.utils import crit_to_multiplier, defense_reduction_to_multiplier
from src.layers.core.term_base import TermBase

DEFAULT_PRIORITY = 10
MAX_PRIORITY = 32


class NaiveSkill:
    def __init__(self, name:str, class_name:str, default_damage:int=0,
                  default_coefficient:float=0, cooldown:int=0,
                  triggered_actions=None, terms:list[TermBase]=list(), **kwargs):
        self._class_name = class_name
        self._name = name
        self._default_damage = default_damage
        self._default_coefficient = default_coefficient
        self._base_cooldown = seconds_to_ticks(cooldown)
        self._actual_cooldown = self._base_cooldown
        self._remaining_cooldown = 0.0
        if triggered_actions is None:
          self._triggered_actions = list()
        else:
          self._triggered_actions = triggered_actions
        self._terms = terms
        self._priority = DEFAULT_PRIORITY
        self._buff_applied = False
    
    def __str__(self):
        return f'{self._name}'

    def _validate_skill(self):
        if self._default_damage < 0 or self.default_coefficient < 0:
            warnings.warn("Damage and coefficient cannot be negative", UserWarning)
        
    def _refresh_skill(self):
        warnings.warn("refresh skill method not defined", UserWarning)

    # decorator for property setter
    def _setter_wrapper(setter):
        def wrap(self, *args, **kwargs):
            setter(self, *args, **kwargs)
            self._refresh_skill()
            self._validate_skill()
            return
        return wrap
    
    # names
    @property
    def class_name(self):
        return self._class_name
    @property
    def name(self):
        return self._name
    
    # damage
    @property
    def default_damage(self):
        return self._default_damage
    @default_damage.setter
    @_setter_wrapper
    def default_damage(self, value: int):
        self._default_damage = max(0, value)


    # coefficient
    @property
    def default_coefficient(self):
        return self._default_coefficient
    @default_coefficient.setter
    @_setter_wrapper
    def default_coefficient(self, value: float):
        self._default_coefficient = max(0, value)

    # cooldown
    # TODO: encapsulate
    @property
    def actual_cooldown(self):
        return self._actual_cooldown
    @actual_cooldown.setter
    def actual_cooldown(self, value: float):
        if value < 0:
            warnings.warn(f'Wrong cooldown given, got: {value}', UserWarning)
        self._actual_cooldown = max(0, value)
    @property
    def remaining_cooldown(self):
        return self._remaining_cooldown
    @remaining_cooldown.setter
    def remaining_cooldown(self, value: float):
        #if value < 0:
        #    warnings.warn(f'Wrong cooldown given, got: {value}', UserWarning)
        self._remaining_cooldown = max(0, value)
    def start_cooldown(self, cooldown_reduction):
        self._remaining_cooldown = self._actual_cooldown * (1-cooldown_reduction)
    
    # triggered actions
    @property
    def triggered_actions(self):
        return self._triggered_actions
    @triggered_actions.setter
    def triggered_actions(self, value: list):
        self._triggered_actions = value

    # priority
    @property
    def priority(self):
        return self._priority
    @priority.setter
    def priority(self, value: int):
        if value < 0 or MAX_PRIORITY < value:
            warnings.warn(f'priority out of range, got: {value}', UserWarning)
        self._priority = value
    
    # buff applied
    @property
    def is_buff_applied(self):
        return self._buff_applied
    @is_buff_applied.setter
    def is_buff_applied(self, value:bool):
        self._buff_applied = value
    
    # check dimension of term and given arguments
    def _check_args_dim(self, args:list[list]):
        if len(args) == len(self._terms):
            return True
        else:
            return False

    # deepcopy itself
    def copy(self):
        return copy.deepcopy(self)
    
    # cancel buffs
    def reset(self):
        self._buff_applied = False
        self._actual_cooldown = self._base_cooldown

    # TODO: change multipliers as plugin
    def calc_damage(self, attack_power:int, args_all:list[list]):
        if not self._remaining_cooldown <= 0:
            warnings.warn(f"Damage calculation before cooldown finished, check skill {self.name}", UserWarning)
        if not self._buff_applied:
            warnings.warn("Damage calculation before buff applied", UserWarning)
        if not self._check_args_dim(args_all):
            raise AttributeError(f'Given arguments\' dimension does not match with num of terms')
        calculated_terms:list[float] = list()
        for term, args in zip(self._terms, *args_all):
            calculated_terms[term.name] = term.get_multiplier(*args)
        damage = self.default_damage + attack_power * self.default_coefficient
        for calculated_term in calculated_terms:
            damage *= calculated_term
        return damage

    def print_skill_info(self):
        targets = [self._class_name, self._name]
        for term in self._terms:
            targets.append(term.name)
        print(f'{targets}')


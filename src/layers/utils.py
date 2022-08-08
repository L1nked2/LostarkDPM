"""
Utilization functions for static and dynamic part of simulator
"""

import sys
import io
import random
from src.layers.static.constants import STAT_BY_UPGRAGE_TABLE
import json
import warnings
from functools import wraps

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def initialize_wrapper(name, enable_start=True, enable_end=True):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if enable_start:
                print(f"##### Start Initialization of {name} #####")
            func(*args, **kwargs)
            if enable_end:
                print(f"##### Done Initialization of {name} #####")
        return decorator
    return wrapper

def print_info_wrapper(name):
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            print(f"##### Information of {name} ######")
            func(*args, **kwargs)
        return decorator
    return wrapper

def raise_attribute_error(layer_name, info):
    print(layer_name + ": " + info)
    raise AttributeError

def json_parser(file_path):
    json_file = open(file_path, "r", encoding='utf-8')
    json_content = json.load(json_file)
    return json_content

"""
Factory for generating character
"""
LEGEND_AVATAR_MULTIPLIER = 1.08
class StatFactory:
  def __init__(self, upgrade=25, crit=0, specialization=0, swiftness=0, **kwargs):
    self.character_stat = dict()
    upgrade_table = STAT_BY_UPGRAGE_TABLE
    # stat and weapon_power from equipment
    self.character_stat['stat'] = (upgrade_table['armor'][upgrade] + upgrade_table['accessories'][upgrade]) * LEGEND_AVATAR_MULTIPLIER
    self.character_stat['weapon_power'] = upgrade_table['weapon'][upgrade]
    self.character_stat['combat_stat'] = {
      'crit': crit,
      'specialization': specialization,
      'swiftness': swiftness,
      'domination': 0,
      'endurance': 0,
      'expertise': 0
    }

class CharacterFactory(StatFactory):
  def __init__(self, class_name, engravings, artifact_set, skill_set, **kwargs):
    super(CharacterFactory, self).__init__(**kwargs)
    self.class_name = class_name
    self.engravings = engravings
    if 'options' in kwargs:
      for option in kwargs['options']:
        self.engravings.append(option)
    self.artifact_set = artifact_set
    self.skill_set = skill_set
  
  def build_dict(self):
    return self.__dict__


"""
Simple crit stats to multiplier helper
"""
def crit_to_multiplier(crit_rate, crit_damage):
  if crit_rate < 0 or crit_damage < 0:
    warnings.warn("Critrate and crit damage must be positive")
    crit_rate = 0
    crit_damage = 0
  crit_rate = min(crit_rate, 1.0)
  return crit_rate * crit_damage + (1 - crit_rate) * 1.0

"""
Import characterss from file_path
returns list of dictionary contaning configuration of each character
"""
def import_character(file_path):
  json_content = json.load(open(file_path, 'r', encoding='utf-8'))
  characters = list()
  for setting in json_content['character_settings']:
    character = CharacterFactory(**setting)
    characters.append(character)
  return characters


"""
Random function for probability
"""
def check_chance(probability):
  if random.random() < probability:
    return True
  return False





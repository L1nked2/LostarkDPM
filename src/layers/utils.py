import sys
import io
from db.constants.common import STAT_BY_UPGRAGE_TABLE
import json
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
class StatFactory:
  def __init__(self, upgrade=25, crit=0, specialization=0, swiftness=0):
    self.character_stat = dict()
    upgrade_table = STAT_BY_UPGRAGE_TABLE
    # stat and weapon_power from equipment
    self.character_stat['stat'] = upgrade_table['armor'][upgrade] + upgrade_table['accessories'][upgrade]
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
  def __init__(self, class_name, engravings, artifact_set, skill_tree, **kwargs):
    super(CharacterFactory, self).__init__(**kwargs)
    self.class_name = class_name
    self.engravings = engravings
    self.artifact_set = artifact_set
    self.skill_tree = skill_tree
  
  def build_dict(self):
    return self.__dict__

"""
Import simulations from file_path
returns list of dictionary contaning configuration of each simulation
"""
def import_simulation(file_path):
  json_content = json.load(open(file_path, 'r', encoding='utf-8'))
  configs = list()
  for sim in json_content['simulations']:
    config = CharacterFactory(**sim)
    configs.append(config)
  return configs
  




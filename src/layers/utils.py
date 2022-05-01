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

def json_parser(file_path):
    json_file = open(file_path, "r", encoding='utf-8')
    json_content = json.load(json_file)
    return json_content

"""
Factory for generating character
character = CharacterFactory(upgrade = #, crit = #, specialization = #, swiftness = #).get_data()
"""
class StatFactory:
    def __init__(self, upgrade=25, crit=0, specialization=0, swiftness=0):
        self.stat = dict()
        upgrade_table = STAT_BY_UPGRAGE_TABLE
        # stat and weapon_power from equipment
        self.stat['stat'] = upgrade_table['armor'][upgrade] + upgrade_table['accessories'][upgrade]
        self.stat['weapon_power'] = upgrade_table['weapon'][upgrade]
        self.stat['combat_stat'] = {
            'crit': crit,
            'specialization': specialization,
            'swiftness': swiftness,
            'domination': 0,
            'endurance': 0,
            'expertise': 0
        }
        
    def get_data(self):
        return self.stat

class CharacterFactory(StatFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        return




import sys
import io

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
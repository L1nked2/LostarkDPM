import json
from collections import OrderedDict
from pprint import pprint

# print korean without broken
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

file_path = "./db/skills/warlord.json"

with open(file_path, "r", encoding="UTF-8") as json_file:
    skill_data = json.load(json_file, object_pairs_hook=OrderedDict)
    pprint(skill_data)
    
    buff_table = skill_data['skill_buff_table']
    pprint(buff_table)

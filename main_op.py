import os
import sys
import csv
import pandas as pd
from tqdm import tqdm
from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.dynamic.damage_history import TIME_LINSPACE, EDPS_LINSPACE, EDPS_MIN_SECONDS, EDPS_MAX_SECONDS
from src.layers.static.character_layer import CharacterLayer
from pyqt5.translator import translator
from src.layers.utils import import_character, CharacterFactory

def get_max_damage_values(damage_history: list):
  max_damage_values = [0, 0, 0, 0]
  damage_event: dict
  for damage_event in damage_history:
    name = damage_event['name']
    damage = damage_event['damage_value']
    is_awakening = damage_event['is_awakening']
    if is_awakening:
      if max_damage_values[3] < damage:
        max_damage_values[2] = name
        max_damage_values[3] = damage
    else:
      if max_damage_values[1] < damage:
        max_damage_values[0] = name
        max_damage_values[1] = damage
  return max_damage_values

if __name__ == '__main__':
    max_damages_csv_path = open('max_damages_critall.csv', 'w', newline='')
    characters_root_path = './db/characters/'
    character_file_names = os.listdir(characters_root_path)
    translator_instance = translator()
    max_damages_df = pd.DataFrame(columns=['classname_kor', 'classname_eng', 'name_normal', 'damage_normal', 'name_awakening', 'damage_awakening'])

    for character_file_name in (progress_bar := tqdm(character_file_names)):
      progress_bar.desc = character_file_name
      character_configs = import_character(characters_root_path + character_file_name)
      character_config: CharacterFactory
      for character_config in character_configs:
        character_dict = character_config.build_dict()
        character_dict['character_stat']['combat_stat']['crit'] = 10000
        simulator = DpmSimulator(character_dict, verbose=0)
        simulator.run_simulation()
        skill_set = os.path.basename(character_dict['skill_set'])
        classname_kor = translator_instance.get_kor_classname(skill_set)[1]
        classname_eng = translator_instance.get_eng_classname(skill_set)[1]
        max_damage_values = get_max_damage_values(simulator.damage_history.get_history())
      max_damages_df.loc[len(max_damages_df.index)] = [classname_kor, classname_eng] + max_damage_values
    
    max_damages_df.to_csv(max_damages_csv_path)
      
        

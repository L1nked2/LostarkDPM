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
    std_out_temp = sys.stdout
    sys.stdout = open('results.txt', 'w')
    dps_csv_path = open('results.csv', 'w', newline='')
    edps_csv_path = open('edps_kor.csv', 'w', newline='')
    max_damages_csv_path = open('max_damages.csv', 'w', newline='')
    characters_root_path = './db/characters/'
    character_file_names = os.listdir(characters_root_path)
    translator_instance = translator()

    result_columns = ['classname_kor', 'classname_eng', 'actual_dps', 'short_dps', 'long_dps', 'nuking_dps', 'edps', 'edps_time_length']
    result_dps_table = pd.DataFrame(columns=result_columns)
    dps_all_df = pd.DataFrame(columns=['classname_kor', 'classname_eng'] + TIME_LINSPACE)
    max_damages_df = pd.DataFrame(columns=['classname_kor', 'classname_eng', 'name_normal', 'damage_normal', 'name_awakening', 'damage_awakening'])

    for character_file_name in (progress_bar := tqdm(character_file_names)):
      progress_bar.desc = character_file_name
      character_configs = import_character(characters_root_path + character_file_name)
      character_config: CharacterFactory
      for character_config in character_configs:
        character_dict = character_config.build_dict()
        simulator = DpmSimulator(character_dict, verbose=0)
        print(f'target_character: {character_file_name}')
        print('==========================')
        simulator.run_simulation()
        simulator.print_result()
        print('==========================')
        simulator.print_damage_details()
        simulator.print_delay_statistics()
        simulator.print_nuking_cycle()
        edps_statistics = simulator.damage_history.get_edps_statistics(EDPS_MIN_SECONDS, EDPS_MAX_SECONDS)
        print('eDPS info: ', [max(edps_statistics), EDPS_LINSPACE[edps_statistics.index(max(edps_statistics))]])
        print('==========================')
        skill_set = os.path.basename(character_dict['skill_set'])
        classname_kor = translator_instance.get_kor_classname(skill_set)[1]
        classname_eng = translator_instance.get_eng_classname(skill_set)[1]        
        result = [classname_kor, classname_eng] + simulator.get_result()
        result += [max(edps_statistics), EDPS_LINSPACE[edps_statistics.index(max(edps_statistics))]]
        result_dps_table.loc[character_file_name] = result
        max_damage_values = get_max_damage_values(simulator.damage_history.get_history())
        dps_all_df.loc[character_file_name] = [classname_kor, classname_eng] + simulator.damage_history.get_edps_statistics(6, 120)
        max_damages_df.loc[len(max_damages_df.index)] = [classname_kor, classname_eng] + max_damage_values
    
    result_dps_table = result_dps_table.sort_values(by=['actual_dps'], ascending=False)
    dps_all_df.to_csv(edps_csv_path)
    result_dps_table.to_csv(dps_csv_path)
    max_damages_df.to_csv(max_damages_csv_path)

      
        

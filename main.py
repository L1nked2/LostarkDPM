import os
import sys
import csv
from tqdm import tqdm
from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.static.character_layer import CharacterLayer
from pyqt5.translator import translator
from src.layers.utils import import_character, CharacterFactory


if __name__ == '__main__':
    std_out_temp = sys.stdout
    sys.stdout = open('results.txt', 'w')
    result_csv = open('results.csv', 'w', newline='')
    csv_wrt = csv.writer(result_csv)
    csv_wrt.writerow(['classname_kor', 'classname_eng', 'actual_dps', 'short_dps', 'long_dps', 'nuking_dps'])
    characters_root_path = './db/characters/'
    character_file_names = os.listdir(characters_root_path)
    translator_instance = translator()
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
        skill_set = os.path.basename(character_dict['skill_set'])
        classname_kor = translator_instance.get_kor_classname(skill_set)[1]
        classname_eng = translator_instance.get_eng_classname(skill_set)[1]
        result = [classname_kor, classname_eng] + simulator.get_result()
        csv_wrt.writerow(result)
        print('==========================')
        simulator.print_damage_details()
        simulator.print_delay_statistics()
        simulator.print_nuking_cycle()
        print('==========================')

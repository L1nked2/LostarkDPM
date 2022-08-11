import os
import sys
from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.static.character_layer import CharacterLayer
from src.layers.utils import import_character


if __name__ == '__main__':
    sys.stdout = open('results.txt', 'w')
    characters_root_path = './db/characters/'
    character_file_names = os.listdir(characters_root_path)
    for character_file_name in character_file_names:
      character_configs = import_character(characters_root_path + character_file_name)

      for character_config in character_configs:
        character_dict = character_config.build_dict()
        simulator = DpmSimulator(character_dict, verbose=False)
        print(f'target_character: {character_file_name}')
        print('==========================')
        simulator.run_simulation()
        simulator.print_result()
        print('==========================')
        simulator.print_damage_details()
        simulator.print_delay_statistics()
        simulator.print_nuking_cycle()
        print('==========================')
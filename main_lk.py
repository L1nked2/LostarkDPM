from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.static.character_layer import CharacterLayer
from src.layers.utils import import_character


if __name__ == '__main__':
    #character_path = './characters.json'
    character_path = './db/characters/character_battlemaster_first_intention.json'
    character_configs = import_character(character_path)

    for character_config in character_configs:
      character_dict = character_config.build_dict()
      #character_dict['artifact_set'] = ['악몽A_6_3']
      simulator = DpmSimulator(character_dict, verbose=False)
      simulator = DpmSimulator(character_dict, max_tick=15000, verbose=True)
      simulator.test()
      print('==========================')
      simulator.run_simulation()
      simulator.print_result()
      print('==========================')
      simulator.print_damage_details()
      simulator.print_delay_statistics()
      simulator.print_nuking_cycle()
      print('==========================')
      

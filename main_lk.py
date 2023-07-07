from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.static.character_layer import CharacterLayer
from src.layers.utils import import_character, CharacterFactory
from src.layers.dynamic.damage_history import EDPS_LINSPACE

if __name__ == '__main__':
    
    character_path = './db/characters/character_aeromancer_gale_rage_dom.json'
    character_path = './db/characters/character_battlemaster_first_intention.json'
    #character_path = './db/characters/character_aeromancer_gale_rage_hal.json'
    character_configs = import_character(character_path)
    character_config: CharacterFactory
    for character_config in character_configs:
      character_dict = character_config.build_dict()
      #character_dict['artifact_set'] = ['악몽A_6_3']
      simulator = DpmSimulator(character_dict, verbose=0)
      #simulator = DpmSimulator(character_dict, max_seconds=150, verbose=1)
      simulator.print_test_info()
      print('==========================')
      simulator.run_simulation()
      simulator.print_result()
      print('==========================')
      simulator.print_damage_details()
      simulator.print_delay_statistics()
      simulator.print_nuking_cycle()
      print('==========================')
      edps_statistics = simulator.damage_history.get_edps_statistics(8, 16)
      #print([x['name'] for x in simulator.damage_history.get_subhistory(12.7).max_cycle])
      print([max(edps_statistics), EDPS_LINSPACE[edps_statistics.index(max(edps_statistics))]])

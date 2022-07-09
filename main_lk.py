from src.layers.dynamic.dpm_simulator import DpmSimulator
from src.layers.static.character_layer import CharacterLayer
from src.layers.utils import import_character


if __name__ == '__main__':
    character_path = './characters.json'
    character_configs = import_character(character_path)

    print(character_configs[0].build_dict())
    temp = CharacterLayer(**character_configs[0].build_dict())
    temp.print_layer_info()

    simulator_config = {
        'tick': 1,
    }
    simulator = DpmSimulator(simulator_config, temp)
    simulator.test()

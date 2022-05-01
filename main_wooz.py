from numpy import character
from src.layers.dynamic import dpm_simulator as simulator
from src.layers.static.info_layer import InfoLayer



if __name__ == '__main__':
    stat = {
        'stat': 10000,
        'weapon_power': 10000,
        'combat_stat': {
            'crit': 300,
            'specialization': 700,
            'domination': 0,
            'swiftness': 1200,
            'endurance': 0,
            'expertise': 0
        }
    }

    skill_tree = "./db/skills/warlord_gogi.json"

    engravings = [
        {
            'engraving_name': '원한',
            'engraving_type': 'static',
            'engraving_target': ['attack_power'],
            'engraving_effect': [(lambda x: x * 1.2)]
        }
    ]


    info = InfoLayer(
        character_stat=stat,
        engravings=engravings,
        artifact_set=None,
        accessories=None,
        skill_tree=skill_tree
    )

    sim = simulator.DpmSimulator(
        config=None,
        policy=None,
        character_info=info,
        class_name='warlord'
    )
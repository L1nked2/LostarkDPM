from src.layers.dynamic import dpm_simulator as simulator
from src.layers.static.skill_tree_layer import SkillTreeLayer
from src.layers.utils import CharacterFactory


if __name__ == '__main__':
    stat = CharacterFactory(upgrade=20, crit=1600, specialization=0, swiftness=500).get_data()

    skill_tree = "./db/skills/warlord_gogi.json"

    engravings = [
        {
            'engraving_name': '원한',
            'engraving_type': 'static',
            'engraving_target': ['damage_multiplier'],
            'engraving_effect': [(lambda x: x * 1.2)]
        }
    ]

    print(stat)
    temp = SkillTreeLayer(
        character_stat=stat,
        engravings=engravings,
        artifact_set=None,
        accessories=None,
        skill_tree=skill_tree
    )
    print(temp.get_character_detail())
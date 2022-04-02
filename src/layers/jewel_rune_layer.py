from skill_tree_layer import SkilTreeLayer
from utils import initialize_wrapper

# key = level
# value = percent
FROSTFIRE_JEWEL_LEVEL_DICT = {
    1: 3,
    2: 6,
    3: 9,
    4: 12,
    5: 15,
    6: 18,
    7: 21,
    8: 24,
    9: 30,
    10: 40
}

NEMESIS_JEWEL_LEVEL_DICT = {
    1: 2,
    2: 4,
    3: 6,
    4: 8,
    5: 10,
    6: 12,
    7: 14,
    8: 16,
    9: 18,
    10: 20
}


class JewelRuneLayer(SkilTreeLayer):
    @initialize_wrapper("JewelRuneLayer", enable_start=False)
    def __init__(self, jewel_spec, rune_spec, **kwargs):
        super(JewelRuneLayer, self).__init__(**kwargs)
        self.jewel_spec = jewel_spec
        self.rune_spec = rune_spec
        self.validate_jewel_rune()

    # validate specs
    def validate_jewel_rune(self):
        # check the number of jewels
        if len(self.jewel_spec["frostfire"]) + len(self.jewel_spec["nemesis"]) > 11:
            raise Exception("Too many jewels!")
        
        skill_list = super(JewelRuneLayer, self).get_skill_preset_by_name()
        frostfire_jewels = self.jewel_spec["frostfire"]
        nemesis_jewels = self.jewel_spec["nemesis"]
        print(skill_list)

        # we may check duplication -> error or caution?

        disabled_frostfire_jewels = [jewel for jewel in frostfire_jewels if jewel[0] not in skill_list]
        disabled_nemesis_jewels = [jewel for jewel in nemesis_jewels if jewel[0] not in skill_list]
        
        print("Disabled frostfire jewels:", disabled_frostfire_jewels)
        print("Disabled nemesis jewels:", disabled_nemesis_jewels)


    # Update skill damage w.r.t jewel specification
    def update(self):
        pass

if __name__ == '__main__':
    stat = {
        'stat': 10000,
        'weapon_power': 10000,
        'combat_stat': {
            'crit': 1500,
            'specialization': 700,
            'domination': 0,
            'swiftness': 0,
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

    # frostfire - 멸화
    # nemesis   - 홍염
    jewel_spec = {
        "frostfire": [
            ["버스트 캐넌", 7],
            ["스피어 샷", 7],
            ["차지 스팅거", 7],
            ["대쉬 어퍼 파이어", 7]
        ],
        "nemesis": [
            ["버스트 캐넌", 7],
            ["스피어 샷", 7],
            ["차지 스팅거", 7],
            ["증오의 함성", 7],
            ["배쉬", 7]
        ]
    }

    temp = JewelRuneLayer(
        character_stat=stat,
        engravings=engravings,
        artifact_set=None,
        accessories=None,
        skill_tree=skill_tree,
        jewel_spec=jewel_spec,
        rune_spec=None
    )
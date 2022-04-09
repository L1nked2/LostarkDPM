from src.layers.dynamic import dpm_simulator as simulator
from src.layers.static import jewel_rune_layer


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

    temp = jewel_rune_layer.JewelRuneLayer(
        character_stat=stat,
        engravings=engravings,
        artifact_set=None,
        accessories=None,
        skill_tree=skill_tree,
        jewel_spec=jewel_spec,
        rune_spec=None
    )
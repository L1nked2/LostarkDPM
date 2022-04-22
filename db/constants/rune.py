# 질풍 / Rune Agel

from unicodedata import category


RUNE_AGEL = {
    "고급": 0.05,
    "희귀": 0.08,
    "영웅": 0.12,
    "전설": 0.14,
    "유물": 0.16
}

# 속행 / Rune Reide

RUNE_REIDE = {
    "고급": 0.05,
    "희귀": 0.08,
    "영웅": 0.12,
    "전설": 0.14,
    "유물": 0.16
}

# 광분 / Rune Rush

RUNE_RUSH = {
    "고급": 0.05,
    "희귀": 0.08,
    "영웅": 0.12,
    "전설": 0.14,
    "유물": 0.16
}

# 출혈 / Rune Jar

RUNE_JAR = {
    "고급": 0.05,
    "희귀": 0.08,
    "영웅": 0.12,
    "전설": 0.14,
    "유물": 0.16
}

RUNE_ALL = {
    "질풍": RUNE_AGEL,
    "속행": RUNE_REIDE,
    "광분": RUNE_RUSH,
    "출혈": RUNE_JAR,
    "집중": None,
    "단죄": None,
    "심판": None,
    "압도": None,
    "풍요": None,
    "수호": None,
    "정화": None,
}

RUNE_LEVEL_ALL = [
    "고급", "희귀", "영웅", "전설", "유물"
]


def get_rune_effect(category, level):
    return RUNE_ALL[category][level]

def validate_runes(runes):
    for rune in runes:
        category = rune["category"]
        level = rune["level"]
        if category not in RUNE_ALL.keys():
            raise Exception(f"{category} rune is not listed in DB!")
        if level not in RUNE_LEVEL_ALL:
            raise Exception(f"{level} level is not listed in DB!")
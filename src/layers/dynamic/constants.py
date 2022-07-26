""" 
Constants for dynamic part
"""

# constants and hyper parameters for dynamic layers
TICKS_PER_SECOND = 100

"""
Unit transformation
"""
def seconds_to_ticks(seconds):
  return seconds * TICKS_PER_SECOND

def ticks_to_seconds(ticks):
  return ticks / TICKS_PER_SECOND

"""
Jewel convert list
"""
DAMAGE_JEWEL_LIST = [
    0,
    0.03,
    0.06,
    0.09,
    0.12,
    0.15,
    0.18,
    0.21,
    0.24,
    0.30,
    0.40
]

COOLDOWN_JEWEL_LIST = [
    0,
    0.02,
    0.04,
    0.06,
    0.08,
    0.10,
    0.12,
    0.14,
    0.16,
    0.18,
    0.20
]

"""
Rune convert list
"""

# 질풍 / Rune Galewind
RUNE_GW = {
    "고급": 0.05,
    "희귀": 0.08,
    "영웅": 0.12,
    "전설": 0.14
}

# 속행 / Rune Quick Recharge
RUNE_QR = {
    "고급": 'rune_qr_1',
    "희귀": 'rune_qr_2',
    "영웅": 'rune_qr_3',
    "전설": 'rune_qr_4'
}

# 광분 / Rune RAGE
RUNE_RG = {
    "고급": 'rune_rg_1',
    "희귀": 'rune_rg_2',
    "영웅": 'rune_rg_3',
    "전설": 'rune_rg_4'
}

# 출혈 / Rune Bleed
RUNE_BD = {
    "고급": 'rune_bd_1',
    "희귀": 'rune_bd_2',
    "영웅": 'rune_bd_3',
    "전설": 'rune_bd_4',
}

RUNE_ALL = {
    "질풍": RUNE_GW,
    "속행": RUNE_QR,
    "광분": RUNE_RG,
    "출혈": RUNE_BD,
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


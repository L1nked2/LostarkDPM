"""
check buff form of ./base.py
"""

CLASS_BUFF_DICT = {
  'AP_Buff_1': {
    'name': 'AP_Buff',
    'buff_type': 'stat',
    'sources': ['damage_mutiplier', 'movement_speed'],
    'target': 'damage_mutiplier',
    'effect': lambda x,y: x * max(1, (1+(y-1)*0.45)),
    'duration': 5,
    'priority': 3,
  },
  'Synergy_1': {
    'name': 'Synergy',
    'buff_type': 'stat',
    'sources': ['damage_mutiplier', 'movement_speed'],
    'target': 'damage_mutiplier',
    'effect': lambda x,y: x * max(1, (1+(y-1)*0.45)),
    'duration': 6,
    'priority': 3,
  }
}
"""
 # ex) [(target, lambda x: True if x == 'back' else False)]
"skill_buff_table": [
    "on start attack 0.5 for next 1 skills",
    "on finish attack 0.3 for next 1 skills",
    "on finish attack_synergy 0.06 for next 20 skills",
    "on finish attack_synergy 0.12 for next 20 skills"
  ]
"""
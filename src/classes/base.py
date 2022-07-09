"""
buff form
name: name of buff (duplication check)
type: stat, skill, damage
sources: attributes used in calculations
target: attribute that buff modifys
effect: lambda function for main calculation
duration: buff duration in seconds
priority: determines buff calculation priority,
          speed: 0, AP: 1
ex)
'Buff_1': {
    'name': 'Buff',
    'buff_type': 'stat',
    'sources': ['damage_mutiplier', 'movement_speed'],
    'target': 'damage_mutiplier',
    'effect': lambda x,y: x * max(1, (1+(y-1)*0.45)),
    'duration': 5,
    'priority': 1,
  }  
"""

BASE_BUFF_DICT = {
  ###### stat buffs ######
  'Raid_Captain_3': {
    'name': 'Raid_Captain',
    'buff_type': 'stat',
    'sources': ['damage_mutiplier', 'movement_speed'],
    'target': 'damage_mutiplier',
    'effect': lambda x,y: x * max(1, (1+(y-1)*0.45)),
    'duration': 999999,
    'priority': 7,
  },
  ###### skill buffs ######
  'Super_Charge_3': {
    'name': 'Super_Charge',
    'buff_type': 'skill',
    'sources': ['damage_mutiplier', 'movement_speed'],
    'target': 'damage_mutiplier',
    'effect': lambda x,y: x * max(1, (1+(y-1)*0.45)),
    'duration': 999999,
    'priority': 7,
  }
}
"""
Buff bodies of blade
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 5,
    'priority': 3,
  },
  'AP_Buff_1': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_1',
    'duration': 5,
    'priority': 3,
  },
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 6,
    'priority': 3,
  }
}

def specialization(character: CharacterLayer, skill: Skill):
    s = character.get_attribute('specialization')

"""
Actions & Buff bodies of warlord
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 3,
  },
  'Lone_Knight_3': {
    'name': 'lone_knight',
    'buff_type': 'stat',
    'effect': 'lone_knight_3',
    'duration': 999999,
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

# Actions
# 배쉬 공증 및 시너지
def action_1(buff_manager: BuffManager, skill_manager: SkillManager):
  pass

# Buff bodies
def specialization(character: CharacterLayer, skill: Skill):
    s = character.get_attribute('specialization')

def lone_knight_3(character: CharacterLayer, skill: Skill):
    if skill.get_attribute('identity_type') == 'Lance':
      s_acr = skill.get_attribute('additional_crit_rate')
      s_acd = skill.get_attribute('additional_crit_damage')
      skill.update_attribute('additional_crit_rate', s_acr + 0.15)
      skill.update_attribute('additional_crit_damage', s_acd + 0.50)
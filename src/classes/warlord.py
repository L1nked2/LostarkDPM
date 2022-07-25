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
    'priority': 7,
  },
  'Lone_Knight_3': {
    'name': 'lone_knight',
    'buff_type': 'stat',
    'effect': 'lone_knight_3',
    'duration': 999999,
    'priority': 7,
  },
  'AP_Buff_1': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_1',
    'duration': 5,
    'priority': 9,
  },
  'AP_Buff_2': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_2',
    'duration': 4,
    'priority': 7,
  },
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 10,
    'priority': 7,
  },
  'Synergy_2': {
    'name': 'synergy_2',
    'buff_type': 'stat',
    'effect': 'synergy_2',
    'duration': 12,
    'priority': 7,
  }
}

# Actions
# 배쉬 공증 및 시너지
def action_1(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_1'], 'class')
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 증오의 함성 시너지
def action_2(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_2'], 'class')

# 대쉬 어퍼 파이어 공증
def action_3(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_2'], 'class')

# Buff bodies
def specialization(character: CharacterLayer, skill: Skill):
    s = character.get_attribute('specialization')

def lone_knight_3(character: CharacterLayer, skill: Skill):
    if skill.get_attribute('identity_type') == 'Lance':
      s_acr = skill.get_attribute('additional_crit_rate')
      s_acd = skill.get_attribute('additional_crit_damage')
      skill.update_attribute('additional_crit_rate', s_acr + 0.15)
      skill.update_attribute('additional_crit_damage', s_acd + 0.50)

# 배쉬 공증
def ap_buff_1(character: CharacterLayer, skill: Skill):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.335 * (1 + c_aap))

# 대쉬 어퍼 파이어 공증
def ap_buff_2(character: CharacterLayer, skill: Skill):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.229 * (1 + c_aap))

# 배쉬 시너지
def synergy_1(character: CharacterLayer, skill: Skill):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.066)

# 증오의 함성 시너지
def synergy_2(character: CharacterLayer, skill: Skill):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('back_attack') == True or skill.get_attribute('head_attack') == True:
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.03)
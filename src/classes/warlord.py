"""
Actions & Buff bodies of warlord
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

SPEC_COEF = 1 / 6.3591 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Combat_Readiness_Full_1': {
    'name': 'combat_readiness',
    'buff_type': 'stat',
    'effect': 'combat_readiness_full_1',
    'duration': 999999,
    'priority': 7,
  },
  'Combat_Readiness_1': {
    'name': 'combat_readiness',
    'buff_type': 'stat',
    'effect': 'combat_readiness_1',
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
    'duration': 6,
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

######## Finalize Skill #########
# finalize skill by tripod and rune
def finalize_skill(skill: Skill):
  name  = skill.get_attribute('name')
  tripod = skill.get_attribute('tripod')
  rune = skill.get_attribute('rune')
  # connect actions
  
  # apply tripods
  if name == '배쉬':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_synergy')
    if tripod[1] == '1':
      skill.triggered_actions.append('activate_ap_buff')
  elif name == '대쉬 어퍼 파이어':
    if tripod[0] == '3':
      skill.triggered_actions.append('activate_ap_buff')
  elif name == '증오의 함성':
    if tripod[2] == '1':
      skill.triggered_actions.append('activate_synergy')
  elif name == '파이어 불릿':
    if tripod[0] == '2':
      skill.triggered_actions.append('lucky_chance_action')

######## Actions #########
# 배쉬, 대쉬 어퍼 파이어 공증
def activate_ap_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '배쉬':
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_1'], 'class')
  elif skill_on_use.get_attribute('name') == '대쉬 어퍼 파이어':
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_2'], 'class')

# 배쉬, 증오의 함성 시너지
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '배쉬':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')
  elif skill_on_use.get_attribute('name') == '증오의 함성':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_2'], 'class')

# 파이어불릿 1트포 행운의 기회
def lucky_chance_action(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    n = skill.get_attribute('name')
    if n == '파이어 불릿':
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(4.9))
    return
  if check_chance(0.75, '파이어 불릿'):
    skill_manager.apply_function(cooldown_reduction)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * SPEC_COEF)
    s_multiplier_2 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    if skill.get_attribute('identity_type') == 'Common':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_2)

def combat_readiness_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('damage_multiplier', s_dm * 1.25 * 1.06)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.06)

def combat_readiness_3(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('damage_multiplier', s_dm * 1.30 * 1.12)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.12)

def lone_knight_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('identity_type') == 'Lance':
      s_acr = skill.get_attribute('additional_crit_rate')
      s_acd = skill.get_attribute('additional_crit_damage')
      skill.update_attribute('additional_crit_rate', s_acr + 0.15)
      skill.update_attribute('additional_crit_damage', s_acd + 0.50)

# 배쉬 공증
def ap_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.335 * (1 + c_aap))

# 대쉬 어퍼 파이어 공증
def ap_buff_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.23 * (1 + c_aap))

# 배쉬 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.066)

# 증오의 함성 시너지
def synergy_2(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('back_attack') == True or skill.get_attribute('head_attack') == True:
      skill.update_attribute('damage_multiplier', s_dm * 1.09)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.04)
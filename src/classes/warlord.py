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

# 파이어불릿 1트포 행운의 기회
def action_4(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
    n = skill.get_attribute('name')
    if n == '파이어 불릿':
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(4.9))
    return
  if check_chance(0.50):
    skill_manager.apply_function(cooldown_reduction)
  if check_chance(0.50):
    skill_manager.apply_function(cooldown_reduction)

# Buff bodies
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

def combat_readiness_full_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('damage_multiplier', s_dm * 1.20 * 1.12)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.12)

def combat_readiness_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('damage_multiplier', s_dm * 1.20)

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
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.03)
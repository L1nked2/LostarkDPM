"""
Actions & Buff bodies of destroyer
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 코어 해방 스킬 피해 증가 특화 계수
SPEC_COEF_1 = 1 / 12.157 / 100
# 중력가중 피해량 특화 계수
SPEC_COEF_2 = 1 / 12.944 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 파스 방감 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 10,
    'priority': 7,
  },
  'Rage_Hammer_3': {
    'name': 'rage_hammer',
    'buff_type': 'stat',
    'effect': 'rage_hammer_3',
    'duration': 999999,
    'priority': 7,
  },
}

######## Finalize Skill #########
# finalize skill by tripod and rune
def finalize_skill(skill: Skill):
  name  = skill.get_attribute('name')
  tripod = skill.get_attribute('tripod')
  rune = skill.get_attribute('rune')
  # connect actions
  # apply tripods
  if name == '파워 스트라이크':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_synergy')

######## Actions #########
# 방깎 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '파워 스트라이크':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_gravity_release = (1 + 0.45 * (1 + s * SPEC_COEF_1))
    s_gravity = (1 + s * SPEC_COEF_2)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == "Gravity_Release":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_gravity_release)
    elif skill.get_attribute('identity_type') == "Gravity":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_gravity)

# 분노의 망치 버프
def rage_hammer_3(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Gravity_Release':
      s_acr = skill.get_attribute('additional_crit_rate')
      s_acd = skill.get_attribute('additional_crit_damage')
      skill.update_attribute('additional_crit_rate', s_acr + 0.15)
      skill.update_attribute('additional_crit_damage', s_acd + 0.45)

# 방감 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.066)

"""
Actions & Buff bodies of berserker
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 폭주 지속 시간 특화 계수
SPEC_COEF_1 = 1 / 5.592 / 100
# 블러디 러쉬 피해량 특화 계수
SPEC_COEF_2 = 1 / 5.825 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 레더 공증 버프
  'AP_Buff_1': {
    'name': 'AP_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_1',
    'duration': 6,
    'priority': 7,
  },
  # 레더 치적 버프
  'Crit_Buff_1': {
    'name': 'crit_buff',
    'buff_type': 'stat',
    'effect': 'crit_buff_1',
    'duration': 6,
    'priority': 9,
  },
  # 체소 치적 버프
  'Crit_Buff_2': {
    'name': 'crit_buff',
    'buff_type': 'stat',
    'effect': 'crit_buff_2',
    'duration': 3,
    'priority': 7,
  },
  # 레더 피증 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 16,
    'priority': 7,
  },
  # 화염 폭풍 데미지 버프
  'Flame_Storm': {
    'name': 'flame_storm',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 591,
    'coefficient': 3.664,
    'damage_interval': 1,
    'duration': 6,
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
  if name == '레드 더스트':
    skill.triggered_actions.append('activate_ap_buff')
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_synergy')
    if tripod[1] == '1':
      skill.triggered_actions.append('activate_crit_buff')
  elif name == '체인 소드':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_crit_buff')
  elif name == '소드 스톰':
    if tripod[2] == '1':
      skill.triggered_actions.append('action_1')

######## Actions #########
# 피증 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '레드 더스트':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 레더 공증 버프 등록
def activate_ap_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '레드 더스트':
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_1'], 'class')

# 레더, 체소 치적 버프 등록
def activate_crit_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '레드 더스트':
    buff_manager.register_buff(CLASS_BUFF_DICT['Crit_Buff_1'], 'class')
  elif skill_on_use.get_attribute('name') == '체인 소드':
    buff_manager.register_buff(CLASS_BUFF_DICT['Crit_Buff_2'], 'class')

# 소드 스톰 3트포 action
def action_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Flame_Storm'], 'class')

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_bloody_rush_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    if skill.get_attribute('name') == "블러디 러쉬":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_bloody_rush_multiplier)      

# 레더 공증 버프
def ap_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.24 * (1 + c_aap))

# 레더 치적 버프
def crit_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('additional_crit_rate')
    skill.update_attribute('additional_crit_rate', s_acr + 0.332)

# 체소 치적 버프
def crit_buff_2(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('additional_crit_rate')
    skill.update_attribute('additional_crit_rate', s_acr + 0.332)

# 피증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)

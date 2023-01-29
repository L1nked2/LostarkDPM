"""
Actions & Buff bodies of demonic
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 기본 변신 시간
DEFAULT_TRANSFORM_TIME_LIMIT = 20

# 악마 스킬 데미지 특화 계수
SPEC_COEF_1 = 1 / 11.65 / 100
# 변신 시간 특화 계수
SPEC_COEF_2 = 1 / 23.3 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 8,
    'priority': 7,
  },
  'Synergy_2': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 16,
    'priority': 7,
  },
  'Speed_Buff_1': {
    'name': 'speed_buff',
    'buff_type': 'stat',
    'effect': 'speed_buff_1',
    'duration': 6,
    'priority': 9,
  },
  'Demon_State': {
    'name': 'demon_state',
    'buff_type': 'stat',
    'effect': 'demon_state',
    'duration': 999999,
    'priority': 9,
  },
  'Perfect_Suppression_1': {
    'name': 'perfect_suppression',
    'buff_type': 'stat',
    'effect': 'perfect_suppression_1',
    'duration': 999999,
    'priority': 7,
  },
  'Demonic_Impulse_3': {
    'name': 'demonic_impulse',
    'buff_type': 'stat',
    'effect': 'demonic_impulse_3',
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
  if name == '악마화 변신':
    skill.triggered_actions.append('demon_transform')
  if name == '악마화 해제':
    skill.triggered_actions.append('recover_human_form')
  if name == '루인 러쉬' or name == '데스 클로':
    skill.triggered_actions.append('activate_synergy')
  if name == '데모닉 슬래쉬':
    skill.triggered_actions.append('grant_transform')
  # apply tripods
  if name == '데모닉 슬래쉬':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_synergy')
    if tripod[1] == '3':
      skill.triggered_actions.append('activate_speed_buff')
  if name == '하울링':
    if tripod[0] == '3':
      skill.triggered_actions.append('activate_synergy')


######## Actions #########
# 데모닉 슬래쉬, 하울링 피증 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '데모닉 슬래쉬':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')
  elif skill_on_use.get_attribute('name') == '하울링':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_2'], 'class')

# 슬래쉬 이속 버프 등록
def activate_speed_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Speed_Buff_1'], 'class')

# 악마화 변신 가능 action
def grant_transform(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
     if skill.get_attribute('name') == '악마화 변신':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 악마화 변신 action
def demon_transform(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  s_multiplier = 1 + buff_manager.character_specialization * SPEC_COEF_2
  transform_time_limit = DEFAULT_TRANSFORM_TIME_LIMIT * s_multiplier
  buff_manager.register_buff(CLASS_BUFF_DICT['Demon_State'], 'class')
  def set_time_limit(skill: Skill):
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('remaining_cooldown', 999999)
    if skill.get_attribute('name') == '악마화 해제':
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(transform_time_limit))
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('identity_type') == 'Demon':
      skill.update_attribute('remaining_cooldown', 0)
  # 악마화 변신, 충동 각인 있을 시 악마 스킬 쿨 초기화
  skill_manager.apply_function(set_time_limit)
  if buff_manager.is_buff_exists('demonic_impulse'):
    skill_manager.apply_function(cooldown_reduction)

# 악마화 해제 action
def recover_human_form(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.unregister_buff('demon_state')
  def recover_cooldown(skill: Skill):
    if skill.get_attribute('identity_type') == 'Common':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(recover_cooldown)
  
######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_demon_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Demon':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_demon_multiplier)

# 데모닉 슬래쉬 피증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)

# 데모닉 슬래쉬 공이속 버프
def speed_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('movement_speed', c_ms + 0.3)

# 악마화 버프
def demon_state(character: CharacterLayer, skill: Skill, buff: Buff):
  c_ms = character.get_attribute('movement_speed')
  character.update_attribute('movement_speed', c_ms + 0.2)

# 완벽한 억제 버프
def perfect_suppression_1(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Common':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.20)

# 멈출 수 없는 충동 버프
def demonic_impulse_3(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Demon':
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('additional_crit_rate', s_acr + 0.3)
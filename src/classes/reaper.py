"""
Actions & Buff bodies of reaper
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 급습 스킬 피해량 특화 계수
SPEC_COEF_1 = 1 / 24.103 / 100

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
  'Persona': {
    'name': 'persona',
    'buff_type': 'stat',
    'effect': 'persona',
    'duration': 10,
    'priority': 7,
  },
  'Tailwind': {
    'name': 'tailwind',
    'buff_type': 'stat',
    'effect': 'tailwind',
    'duration': 4,
    'priority': 9,
  },
  # 오류 출력 방지용 달소 버프(더미)
  'Lunar_Voice_3': {
    'name': 'lunar_voice',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  # 갈증 버프, 아덴 자체 효과도 통합되어있음
  'Hunger_3': {
    'name': 'hunger',
    'buff_type': 'stat',
    'effect': 'hunger_3',
    'duration': 999999,
    'priority': 9,
  },
  # 독: 부식, 상시 3중첩
  'Poison_Corrosion': {
    'name': 'poison_corrosion',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 7,
    'coefficient': 0.45,
    'damage_interval': 1,
    'duration': 8,
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
  if name == '어둠 게이지 체크':
    skill.triggered_actions.append('grant_persona')
  if name == '페르소나 상태 진입':
    skill.triggered_actions.append('activate_persona')
  if skill.get_attribute('identity_type') == 'Swoop':
    skill.triggered_actions.append('deactivate_persona')
  # apply tripods
  if name == '나이트메어' or name == '나이트메어_1타':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_poison')
      skill.triggered_actions.append('activate_synergy')
  elif name == '쉐도우 닷' or name == '쉐도우 닷_1타':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_poison')
      skill.triggered_actions.append('activate_synergy')
    if tripod[2] == '2':
      skill.triggered_actions.append('swoop_activation')
  elif name == '디스토션':
    if tripod[1] == '2':
      skill.triggered_actions.append('activate_tailwind')
  elif name == '쉐도우 트랩':
    if tripod[2] == '2':
      skill.triggered_actions.append('shadow_activation')

######## Actions #########
# 페르소나 사용 가능 전환
def grant_persona(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '페르소나 상태 진입':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 페르소나 사용
def activate_persona(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Persona'], 'class')

# 급습 사용시 페르소나 해제
def deactivate_persona(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '어둠 게이지 체크':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 방깎 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 부식 독 데미지 버프 등록
def activate_poison(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Poison_Corrosion'], 'class')

# 쉐도우 닷 급습 활성
def swoop_activation(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('identity_type') == 'Swoop':
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(1.9))
  skill_manager.apply_function(cooldown_reduction)

# 트랩 그림자 활성
def shadow_activation(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('identity_type') == 'Shadow':
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(2.4))
  skill_manager.apply_function(cooldown_reduction)

# 디스토션 순풍 버프 등록
def activate_tailwind(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Tailwind'], 'class')

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_swoop_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == "Swoop":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_swoop_multiplier)

# 페르소나 버프
def persona(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    character.update_attribute('attack_speed', c_as + 0.1)
    if skill.get_attribute('identity_type') == "Swoop":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 2.6)

# 방깎 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.066)

# 디스토션 순풍
def tailwind(character: CharacterLayer, skill: Skill, buff: Buff):
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('movement_speed', c_ms + 0.3)

# 갈증 및 아덴 자체 버프
def hunger_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    c_cr = character.get_attribute('crit_rate')
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('attack_speed', c_as + 0.1)
    character.update_attribute('movement_speed', c_ms + 0.1)
    character.update_attribute('crit_rate', c_cr + 0.15)
    character.update_attribute('additional_attack_power', c_aap + 0.30 * (1 + c_aap))

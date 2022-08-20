"""
Actions & Buff bodies of blade
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 버스트 특화 계수
SPEC_COEF_1 = 1 / 8.7383 / 100
# 아츠 쿨감 특화 계수
SPEC_COEF_2 = 1 / 34.9655 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Remaining_Energy_Enabled_1': {
    'name': 'remaining_energy_enabled_1',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  'Remaining_Energy_Enabled_3': {
    'name': 'remaining_energy_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  'Remaining_Energy_1': {
    'name': 'remaining_energy',
    'buff_type': 'stat',
    'effect': 'remaining_energy_1',
    'duration': 30,
    'priority': 7,
  },
  'Remaining_Energy_3': {
    'name': 'remaining_energy',
    'buff_type': 'stat',
    'effect': 'remaining_energy_3',
    'duration': 30,
    'priority': 7,
  },
  'Burst_Art': {
    'name': 'burst_art',
    'buff_type': 'stat',
    'effect': 'burst_art',
    'duration': 30,
    'priority': 7,
  },
  'Burst_Enabled_1': {
    'name': 'burst_enabled_1',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  'Burst_Enabled_3': {
    'name': 'burst_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  'Burst_Full_1': {
    'name': 'burst_full',
    'buff_type': 'stat',
    'effect': 'burst_full_1',
    'duration': 999999,
    'priority': 7,
  },
  'Burst_Full_3': {
    'name': 'burst_full',
    'buff_type': 'stat',
    'effect': 'burst_full_3',
    'duration': 999999,
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
    'duration': 6,
    'priority': 7,
  },
  # 블랙 익스플로젼(10멸, 5렙)
  'Black_Explosion': {
    'name': 'black_explosion',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 3564,
    'coefficient': 51.8616,
    'damage_interval': 1,
    'duration': 1,
    'priority': 7,
  },
  # 공허 지대(10멸, 5렙)
  'Void_Zone': {
    'name': 'void_zone',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 3564,
    'coefficient': 1.4175,
    'damage_interval': 1,
    'duration': 5,
    'priority': 7,
  },
}

# Actions
# 이츠 사용가능 상태로 전환
def grant_burst(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '아츠 활성화':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 아츠 활성화
def activate_burst(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.unregister_buff('remaining_energy')
  buff_manager.register_buff(CLASS_BUFF_DICT['Burst_Art'], 'class')
  reduction_percentage = 0.5 * (1 + buff_manager.character_specialization * SPEC_COEF_2)
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('identity_type') == 'Common':
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc * (1 - reduction_percentage))
    if skill.get_attribute('name') == '버스트':
      skill.update_attribute('remaining_cooldown', 0)
    return
  skill_manager.apply_function(cooldown_reduction)

# 버스트 스택 증가
def burst_increase_stack(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def increase_burst_stack(buff: Buff):
    if buff.name == 'burst_art' and buff.stack < 20:
      buff.increase_stack()
    return
  buff_manager.apply_function(increase_burst_stack)

# 버스트 풀 스택 달성
def burst_full(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if buff_manager.is_buff_exists('burst_enabled_1'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Burst_Full_1'], 'class')
  elif buff_manager.is_buff_exists('burst_enabled_3'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Burst_Full_3'], 'class')

# 버스트 사용, 아츠 종료
def use_burst(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.unregister_buff('burst_art')
  buff_manager.unregister_buff('burst_full')
  if buff_manager.is_buff_exists('remaining_energy_enabled_1'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Remaining_Energy_1'], 'class')
  elif buff_manager.is_buff_exists('remaining_energy_enabled_3'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Remaining_Energy_3'], 'class')

# 스핀 커터 시너지 등록
def activate_synergy_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 마엘스톰 시너지 등록
def activate_synergy_2(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_2'], 'class')

# 보이드 스트라이크 3트포 블랙 디멘션 action
def action_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Black_Explosion'], 'class')

# 보이드 스트라이크 2트포 공허 지대 action
def action_2(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Void_Zone'], 'class')

def mael_storm_cooldown_indicator(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '마엘스톰 쿨타임 체크':
      rc = skill.get_attribute('remaining_cooldown')
      skill.start_cooldown
    return
  skill_manager.apply_function(cooldown_reduction)


# Buff bodies
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_multiplier_2 = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('name') == '버스트':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_2)

# 잔재
def remaining_energy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('additional_attack_power', c_aap + 0.25 * (1 + c_aap))
    character.update_attribute('attack_speed', c_as + 0.06)
    character.update_attribute('movement_speed', c_ms + 0.06)

def remaining_energy_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('additional_attack_power', c_aap + 0.36 * (1 + c_aap))
    character.update_attribute('attack_speed', c_as + 0.12)
    character.update_attribute('movement_speed', c_ms + 0.12)

# 아츠 버프
def burst_art(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    ap_coeff = 0.3 + buff.stack * 0.01
    character.update_attribute('additional_attack_power', c_aap + ap_coeff * (1 + c_aap))
    character.update_attribute('attack_speed', c_as + 0.20)
    character.update_attribute('movement_speed', c_ms + 0.10)

# 버스트 풀 스택
def burst_full_1(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('name') == '버스트':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 2.0)

def burst_full_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('name') == '버스트':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 2.2)

# 스핀 커터 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    if skill.get_attribute('back_attack') == True or skill.get_attribute('head_attack') == True:
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
    else:
      skill.update_attribute('damage_multiplier', s_dm * 1.03)

# 마엘스톰 시너지
def synergy_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.25)
    character.update_attribute('movement_speed', c_ms + 0.198)
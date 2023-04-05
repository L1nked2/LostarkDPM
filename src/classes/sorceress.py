"""
Actions & Buff bodies of sorceress
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks, ticks_to_seconds
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 마력 강화 및 마력 해방 속성 피해 효율 특화 계수
SPEC_COEF_1 = 1 / 3.251 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 블레이즈 피증 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 13,
    'priority': 7,
  },
  'Magic_Release': {
    'name': 'magic_release',
    'buff_type': 'stat',
    'effect': 'magic_release',
    'duration': 999999,
    'priority': 9,
  },
  # 점화 각인
  'Igniter_Enabled_3': {
    'name': 'igniter_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  'Igniter_3': {
    'name': 'igniter',
    'buff_type': 'stat',
    'effect': 'igniter_3',
    'duration': 999999,
    'priority': 7,
  },
  # 환류 각인
  'Reflux_3': {
    'name': 'reflux',
    'buff_type': 'stat',
    'effect': 'reflux_3',
    'duration': 999999,
    'priority': 7,
  },
  # 천벌-방전 데미지 버프
  'Electric_Discharge': {
    'name': 'electric_discharge',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 552,
    'coefficient': 2.443,
    'damage_interval': 1,
    'duration': 3,
    'priority': 7,
  },
  # 종말-발화 데미지 버프, 보석 적용x
  'Ignite': {
    'name': 'ignite',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 653,
    'coefficient': 4.049,
    'damage_interval': 1,
    'duration': 5,
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
  if name == '블레이즈':
    if rune == '출혈_전설' or '출혈_영웅':
      skill.triggered_actions.append('extend_bleed')
  elif name == '마력 해방 준비_1':
    skill.triggered_actions.append('grant_magic_release_1')
  elif name == '마력 해방 준비_2':
    skill.triggered_actions.append('grant_magic_release_2')
  elif name == '마력 해방 시작':
    skill.triggered_actions.append('activate_magic_release')
  elif name == '마력 해방 종료':
    skill.triggered_actions.append('deactivate_magic_release')
  # apply tripods
  if name == '블레이즈':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_synergy')
  elif name == '천벌':
    if tripod[1] == '2':
      skill.triggered_actions.append('activate_electric_discharge')
  elif name == '종말의 날_데미지':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_ignite')

######## Actions #########
# 방깎 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '블레이즈':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 블레이즈 출혈 시간 갱신 action
def extend_bleed(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def duration_increase(buff: Buff):
    if buff.name == '출혈':
      buff.duration += seconds_to_ticks(3)
  buff_manager.apply_function(duration_increase)

# 천벌-방전 데미지 버프 등록 action
def activate_electric_discharge(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Electric_Discharge'], skill_on_use)

# 종말-발화 데미지 버프 등록 action
def activate_ignite(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Ignite'], None)

# 마력 해방 사용 가능 전환
def grant_magic_release_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '마력 해방 시작' or skill.get_attribute('name') == '마력 해방 종료':
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(999999))
    elif skill.get_attribute('name') == '마력 해방 준비_2':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

def grant_magic_release_2(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '마력 해방 시작' or skill.get_attribute('name') == '마력 해방 종료':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 마력 해방 시작 action
def activate_magic_release(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  reduction_percentage = 0.25
  # 점화 각인 채용시 추가효과 및 점화 버프
  if buff_manager.is_buff_exists('igniter_enabled_3'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Igniter_3'], skill_on_use)
    reduction_percentage = 0.5
  # 스킬 쿨감
  def cooldown_reduction(skill: Skill):      
    if skill.get_attribute('identity_type') != 'Awakening':
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc * (1 - reduction_percentage))
    return
  skill_manager.apply_function(cooldown_reduction)
  # 마력 해방 버프 등록
  buff_manager.register_buff(CLASS_BUFF_DICT['Magic_Release'], skill_on_use)

# 마력 해방 종료 action
def deactivate_magic_release(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.unregister_buff('magic_release')
  buff_manager.unregister_buff('igniter')
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '마력 해방 준비_1':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)

# 마력 해방 버프
def magic_release(character: CharacterLayer, skill: Skill, buff: Buff):
  # 해방시 딜 증가
  c_s = character.get_attribute('specialization')
  s_dm = skill.get_attribute('damage_multiplier')
  skill.update_attribute('damage_multiplier', s_dm * (1 + (0.18 * (1 + c_s * SPEC_COEF_1))))
  # 시전시간(캐스팅 시간만) 1초 적용, 조정 후 질풍 재적용
  if skill.get_attribute('skill_type') == 'Casting':
    if skill.get_attribute('rune') == '질풍':
      if skill.get_attribute('rune_level') == '전설':
        skill.update_attribute('type_specific_delay', seconds_to_ticks(1) / 1.14)
      elif skill.get_attribute('rune_level') == '영웅':
        skill.update_attribute('type_specific_delay', seconds_to_ticks(1) / 1.12)
    else:
      if skill.get_attribute('type_specific_delay') > 0:
        skill.update_attribute('type_specific_delay', seconds_to_ticks(1))
  # 마력 증폭 트포 적용
  s_n = skill.get_attribute('name')
  if s_n == '종말의 날_데미지' or s_n == '익스플로전' or s_n == '천벌':
    if skill.get_attribute('tripod')[2] == '1':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.2)

# 점화 버프
def igniter_3(character: CharacterLayer, skill: Skill, buff: Buff):
  s_acr = skill.get_attribute('additional_crit_rate')
  s_acd = skill.get_attribute('additional_crit_damage')
  skill.update_attribute('additional_crit_rate', s_acr + 0.25)
  skill.update_attribute('additional_crit_damage', s_acd + 0.50)

# 환류 버프
def reflux_3(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') != 'Awakening':
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.20)
    s_ac = skill.get_attribute('actual_cooldown')
    skill.update_attribute('actual_cooldown', s_ac * (1 - 0.10))

# 피증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)

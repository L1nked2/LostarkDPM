"""
Actions & Buff bodies of aeromancer
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks, ticks_to_seconds
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 기본 여우비 지속 시간
DEFAULT_SUNSHOWER_TIME_LIMIT = 12

# 기상 스킬 피해량 증가 특화 계수
SPEC_COEF_1 = 1 / 13.98 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 이슬비
  'Drizzle_Enabled_3': {
    'name': 'drizzle_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  # 질풍노도
  'Gale_Rage_3': {
    'name': 'gale_rage',
    'buff_type': 'stat',
    'effect': 'gale_rage_3',
    'duration': 999999,
    'priority': 3,
  },
  # 이슬비
  'Drizzle_3': {
    'name': 'drizzle',
    'buff_type': 'stat',
    'effect': 'drizzle_3',
    'duration': DEFAULT_SUNSHOWER_TIME_LIMIT,
    'priority': 7,
  },
  # 돌개바람 치적 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 12,
    'priority': 7,
  },
  # 여우비 아덴 관리용 더미 버프
  # 10스택시 아덴 게이지 풀로 간주
  # 질풍노도는 6개 스킬 사용시 아덴 풀
  # 이슬비는 정해진 사이클에 강제 아덴 채우기 스킬 넣기
  'Rain_Gauge': {
    'name': 'rain_gauge',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  # 여우비 상태 버프
  'Sunshower': {
    'name': 'sunshower',
    'buff_type': 'stat',
    'effect': 'sunshower',
    'duration': DEFAULT_SUNSHOWER_TIME_LIMIT,
    'priority': 7,
  },
  # 여우비 상태 버프(질풍노도 추가 효과)
  'Sunshower_Gale_Rage': {
    'name': 'sunshower_gale_rage',
    'buff_type': 'stat',
    'effect': 'sunshower_gale_rage',
    'duration': DEFAULT_SUNSHOWER_TIME_LIMIT,
    'priority': 7,
  },
  # 여우비 데미지 버프(10멸 기준)
  'Sunshower_Damage': {
    'name': 'sunshower_damage',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 632 * 1.4,
    'coefficient': 3.918 * 1.4,
    'damage_interval': 1,
    'duration': DEFAULT_SUNSHOWER_TIME_LIMIT,
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
  if name != '여우비 활성화':
    skill.triggered_actions.append('check_rain_gauge')
  if name == '여우비 활성화':
    skill.triggered_actions.append('activate_sunshower')
  if name == '여우비 비활성화':
    skill.triggered_actions.append('deactivate_sunshower')
  # apply tripods
  if name == '소나기':
    if tripod[0] == '1':
      for i in range(3):
        skill.triggered_actions.append('check_rain_gauge')
  if name == '소용돌이':
    if tripod[0] == '3':
      for i in range(3):
        skill.triggered_actions.append('check_rain_gauge')
  

######## Actions #########
# 치적 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '돌개바람':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 빗방울 게이지 스택 관리 및 여우비 사용 가능 전환
def check_rain_gauge(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def increase_rain_gauge_stack(buff: Buff):
    if buff.name == 'rain_gauge' and buff.stack < 10:
      buff.increase_stack(1)
    return
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '여우비 활성화':
      skill.update_attribute('remaining_cooldown', 0)
    return
  def initialize_rain_gauge_stack(buff: Buff):
    if buff.name == 'rain_gauge':
      buff.stack = 0
    return
  if not buff_manager.is_buff_exists('rain_gauge'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Rain_Gauge'], 'class')
  if not buff_manager.is_buff_exists('sunshower'):
    buff_manager.apply_function(increase_rain_gauge_stack)
    rain_gauge_buff = buff_manager.get_buff('rain_gauge')
    if rain_gauge_buff is not None and rain_gauge_buff.stack >= 6:
      skill_manager.apply_function(cooldown_reduction)
      buff_manager.apply_function(initialize_rain_gauge_stack)

# 여우비 켜기
def activate_sunshower(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  sunshower_dict = CLASS_BUFF_DICT['Sunshower'].copy()
  sunshower_gale_rage_dict = CLASS_BUFF_DICT['Sunshower_Gale_Rage'].copy()
  sunshower_damage_dict = CLASS_BUFF_DICT['Sunshower_Damage'].copy()
  sunshower_duration = DEFAULT_SUNSHOWER_TIME_LIMIT
  is_sunshower_default = True
  if buff_manager.is_buff_exists('drizzle_enabled_1') or buff_manager.is_buff_exists('drizzle_enabled_3'):
    is_drizzle_enabled = True
  else:
    is_drizzle_enabled = False
  if buff_manager.is_buff_exists('drizzle_enabled_3'):
      drizzle_dict = CLASS_BUFF_DICT['Drizzle_3']
  is_gale_rage_enabled = buff_manager.is_buff_exists('gale_rage')

  if skill_on_use.get_attribute('name') == '여우비 활성화':
    # 여우비 지속 시간 조절 및 질풍노도 적용
    if is_gale_rage_enabled and is_drizzle_enabled:
      is_sunshower_default = False
    elif is_gale_rage_enabled:
      sunshower_duration = sunshower_duration / 1.50
      is_sunshower_default = False
    elif is_drizzle_enabled:
      sunshower_duration = sunshower_duration * 2.00
    # 질풍노도 없을 시 여우비에 기상 스킬 딜증 적용
    # 이슬비 채용시 딜증 적용
    if is_sunshower_default:
      s = buff_manager.character_specialization
      s_multiplier = (1 + s * SPEC_COEF_1)
      if buff_manager.is_buff_exists('drizzle_enabled_3'):
        s_multiplier = s_multiplier * 1.30
      sunshower_damage_dict['base_damage'] = sunshower_damage_dict['base_damage'] * s_multiplier
      sunshower_damage_dict['coefficient'] = sunshower_damage_dict['coefficient'] * s_multiplier
    # 질풍노도 있을 시 추가 공이속 버프 등록
    else:
      sunshower_gale_rage_dict['duration'] = sunshower_duration
      buff_manager.register_buff(sunshower_gale_rage_dict, 'class')
    # 기본 여우비 버프 및 여우비 데미지 버프 등록
    sunshower_dict['duration'] = sunshower_duration
    sunshower_damage_dict['duration'] = sunshower_duration
    buff_manager.register_buff(sunshower_dict, 'class')
    buff_manager.register_buff(sunshower_damage_dict, 'class')
    # 이슬비 활성화시 이슬비 버프 등록
    if is_drizzle_enabled:
      drizzle_dict['duration'] = sunshower_duration
      buff_manager.register_buff(drizzle_dict, 'class')

# 여우비 끄기, 이슬비 소용돌이/소나기 이슬비 버프 미적용 구현용 -> 개선필요
def deactivate_sunshower(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.unregister_buff('sunshower')
  buff_manager.unregister_buff('drizzle')

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_weather_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Weather':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_weather_multiplier)
    
# 돌개바람 치적 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
  s_acr = skill.get_attribute('additional_crit_rate')
  skill.update_attribute('additional_crit_rate', s_acr + 0.10)

# 질풍노도
def gale_rage_3(character: CharacterLayer, skill: Skill, buff: Buff):
  c_ms = character.get_attribute('movement_speed')
  s_acr = skill.get_attribute('additional_crit_rate')
  s_acd = skill.get_attribute('additional_crit_damage')
  skill.update_attribute('additional_crit_rate', s_acr + 0.30 * (c_ms-1))
  skill.update_attribute('additional_crit_damage', s_acd + 0.90 * (c_ms-1))

# 이슬비
def drizzle_3(character: CharacterLayer, skill: Skill, buff: Buff):
  s_dm = skill.get_attribute('damage_multiplier')
  if skill.get_attribute('identity_type') == 'Weather':
    skill.update_attribute('damage_multiplier', s_dm * 1.30)

# 여우비 버프
# 트포로 인한 여우비 상태 추가 딜증 처리
def sunshower(character: CharacterLayer, skill: Skill, buff: Buff):
  s_dm = skill.get_attribute('damage_multiplier')
  if ((skill.get_attribute('name') == '소용돌이' and skill.get_attribute('tripod')[2] == '2')
  or (skill.get_attribute('name') == '센바람' and skill.get_attribute('tripod')[1] == '3')
  or (skill.get_attribute('name') == '싹쓸바람' and skill.get_attribute('tripod')[2] == '1')
  or (skill.get_attribute('name') == '뙤약볕' and skill.get_attribute('tripod')[1] == '1')):
    skill.update_attribute('damage_multiplier', s_dm * 1.20)

# 여우비(질풍노도)의 공이속 시너지 버프
def sunshower_gale_rage(character: CharacterLayer, skill: Skill, buff: Buff):
  c_as = character.get_attribute('attack_speed')
  c_ms = character.get_attribute('movement_speed')
  character.update_attribute('attack_speed', c_as + 0.12)
  character.update_attribute('movement_speed', c_ms + 0.12)

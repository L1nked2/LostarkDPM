"""
Actions & Buff bodies of Summoner
"""
from src.layers.dynamic import skill
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.core.utils import seconds_to_ticks, ticks_to_seconds
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 고대 정령 스킬 피해량 특화 계수
SPEC_COEF_1 = 0.85 / 699
# 슈르디 기본 지속 시간
DEFAULT_SHURDI_DURATION = 20


SKILL_NAME_DICT = {
  '파우루': '파우루',
  '마리린': '마리린',
  '켈시온': '켈시온',
  '파우루_체인': '파우루_체인',
  '마리린_체인': '마리린_체인',
  '켈시온_체인': '켈시온_체인',
}

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 상급 소환사
  'Master_Summoner_3': {
    'name': 'master_summoner',
    'buff_type': 'stat',
    'effect': 'master_summoner_3',
    'duration': 999999,
    'priority': 7,
  },
  # 넘치는 교감
  'Communication_Overflow_3': {
    'name': 'communication_overflow',
    'buff_type': 'stat',
    'effect': 'communication_overflow_3',
    'duration': 999999,
    'priority': 7,
  },
  # 이끼늪 방깎 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 16,
    'priority': 7,
  },
  # 이끼늪, 엘씨드 공증 버프
  'AP_Buff_1': {
    'name': 'AP_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_1',
    'duration': 5,
    'priority': 7,
  },
  # 슈르디 치적 버프
  'Crit_Buff_1': {
    'name': 'crit_buff',
    'buff_type': 'stat',
    'effect': 'crit_buff_1',
    'duration': DEFAULT_SHURDI_DURATION,
    'priority': 7,
  },
  # 폭풍의 질주 데미지 버프, 보석 적용x
  'Stormlike_Gallop': {
    'name': 'stormlike_gallop',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 12 * 0.3,
    'coefficient': 0.074 * 0.3,
    'damage_interval': 1,
    'duration': 5,
    'priority': 7,
  },
  # 파우루(교감, 311) 데미지 버프
  'Blue_Flame_Pauru_CO': {
    'name': 'pauru',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 403 * 0.9251587,
    'coefficient': 2.499 * 0.9251587,
    'damage_interval': 1,
    'duration': 18,
    'priority': 7,
  },
  # 마리린(교감, 212) 데미지 버프
  'Maririn_CO': {
    'name': 'maririn',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 568 * 0.42775,
    'coefficient': 3.522 * 0.42775,
    'damage_interval': 1,
    'duration': 44,
    'priority': 7,
  },
  # 엘씨드(212) 데미지 버프
  'Elite_Elcid': {
    'name': 'elcid',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 137 * 5.782,
    'coefficient': 0.849 * 5.782,
    'damage_interval': 1,
    'duration': 10,
    'priority': 7,
  },
  # 엘씨드(교감, 212) 데미지 버프
  'Elite_Elcid_CO': {
    'name': 'elcid',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 137 * 7.322903,
    'coefficient': 0.849 * 7.322903,
    'damage_interval': 1,
    'duration': 12,
    'priority': 7,
  },
  # 슈르디(332) 데미지 버프
  'Faltering_Shurdi': {
    'name': 'shurdi',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 501 * 0.3214,
    'coefficient': 3.106 * 0.3214,
    'damage_interval': 1,
    'duration': 28,
    'priority': 7,
  },
  # 슈르디(똘똘이, 교감) 데미지 버프
  'Smart_Shurdi_CO': {
    'name': 'shurdi',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 501 * 0.417,
    'coefficient': 3.106 * 0.417,
    'damage_interval': 1,
    'duration': 24,
    'priority': 7,
  },
  # 슈르디(짜릿한 빛, 교감) 데미지 버프
  'Thrilling_Light_CO': {
    'name': 'thrilling_light',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 1489 * 0.125,
    'coefficient': 9.232 * 0.125,
    'damage_interval': 1,
    'duration': 24,
    'priority': 7,
  },
  # 켈시온(교감) 데미지 버프
  'Kelsion_CO': {
    'name': 'kelsion',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 6288 * 0.226,
    'coefficient': 38.986 * 0.226,
    'damage_interval': 1,
    'duration': 24,
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
  if name == '파우루':
    skill.triggered_actions.append('activate_pauru')
  elif name == '엘씨드':
    skill.triggered_actions.append('activate_elcid')
  elif name == '마리린':
    skill.triggered_actions.append('activate_maririn')
  elif name == '슈르디':
    skill.triggered_actions.append('activate_shurdi')
    if rune[:2] =='출혈':
      skill.triggered_actions.append('extend_bleed')
  elif name == '켈시온':
    skill.triggered_actions.append('activate_kelsion')
  if (name == SKILL_NAME_DICT['파우루'] 
      or name == SKILL_NAME_DICT['마리린'] 
      or name == SKILL_NAME_DICT['켈시온']):
    skill.triggered_actions.append('grant_summon_chain')
  elif (name == SKILL_NAME_DICT['파우루_체인'] 
        or name == SKILL_NAME_DICT['마리린_체인'] 
        or name == SKILL_NAME_DICT['켈시온_체인']):
    skill.triggered_actions.append('use_summon_chain')
  # apply tripods
  if name == '끈적이는 이끼늪':
    if tripod[0] == '3':
      skill.triggered_actions.append('activate_ap_buff')
    elif tripod[1] == '1':
      skill.triggered_actions.append('activate_synergy')
  elif name == '마력의 질주':
    if tripod[0] == '2':
      skill.triggered_actions.append('activate_stormlike_gallop')
  elif name == '엘씨드':
    if tripod[0] == '2':
      skill.triggered_actions.append('activate_ap_buff')
  elif name == '슈르디':
    if tripod[0] == '3':
      skill.triggered_actions.append('activate_crit_buff')
      


######## Actions #########
# 슈르디 출혈 시간 갱신 action
def extend_bleed(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 슈르디
  if skill_on_use.get_attribute('name') == '슈르디':
    def duration_increase(buff: Buff):
      if buff.name == '출혈':
        buff.duration += seconds_to_ticks(20)
    buff_manager.apply_function(duration_increase)

# 이끼늪 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '끈적이는 이끼늪' and skill_on_use.get_attribute('tripod')[1] == '1':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 이끼늪, 엘씨드 공증 등록
def activate_ap_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if ((skill_on_use.get_attribute('name') == '끈적이는 이끼늪'and skill_on_use.get_attribute('tripod')[0] == '3')
    or (skill_on_use.get_attribute('name') == '엘씨드'and skill_on_use.get_attribute('tripod')[0] == '2')):
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_1'], skill_on_use)

# 슈르디 - 빛의 성장 치적 버프 등록
def activate_crit_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_dict = CLASS_BUFF_DICT['Crit_Buff_1'].copy()
  if skill_on_use.get_attribute('name') == '슈르디' and skill_on_use.get_attribute('tripod')[0] == '3':
    if skill_on_use.get_attribute('tripod')[1] == '3':
      buff_dict['duration'] = buff_dict['duration'] + 8.0
    elif buff_manager.is_buff_exists('communication_overflow'):
      buff_dict['duration'] = buff_dict['duration'] + 4.0
    buff_manager.register_buff(buff_dict, skill_on_use)

# 소환수 사용시 체인 스킬 사용 가능
def grant_summon_chain(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 교감 체크
  base_cooldown_reduction = (1 - buff_manager.base_character.cooldown_reduction)
  # 스킬별 쿨다운
  pauru_cooldown = 8.0 * base_cooldown_reduction
  maririn_cooldown = 12.0 * base_cooldown_reduction
  kelsion_cooldown = 8.0 * base_cooldown_reduction
  # 각 체인 스킬별 스킬 쿨감
  starting_cooldown = 999999 * base_cooldown_reduction
  
  def cooldown_reduction_pauru(skill: Skill):
    if skill.get_attribute('name') == SKILL_NAME_DICT['파우루_체인']:
      rc = ticks_to_seconds(skill.get_attribute('remaining_cooldown'))
      elapsed_time = starting_cooldown - rc
      if elapsed_time < pauru_cooldown:
        new_cooldown = pauru_cooldown - elapsed_time
      else:
        new_cooldown = 0
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(new_cooldown))
    return
  def cooldown_reduction_maririn(skill: Skill):
    if skill.get_attribute('name') == SKILL_NAME_DICT['마리린_체인']:
      rc = ticks_to_seconds(skill.get_attribute('remaining_cooldown'))
      elapsed_time = starting_cooldown - rc
      if elapsed_time < maririn_cooldown:
        new_cooldown = maririn_cooldown - elapsed_time
      else:
        new_cooldown = 0
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(new_cooldown))
    return
  def cooldown_reduction_kelsion(skill: Skill):
    if skill.get_attribute('name') == SKILL_NAME_DICT['켈시온_체인']:
      rc = ticks_to_seconds(skill.get_attribute('remaining_cooldown'))
      elapsed_time = starting_cooldown - rc
      if elapsed_time < kelsion_cooldown:
        new_cooldown = kelsion_cooldown - elapsed_time
      else:
        new_cooldown = 0
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(new_cooldown))
    return
  # 소환수 스킬 사용시 체인 스킬 사용가능하게 변경
  if skill_on_use.get_attribute('name') == SKILL_NAME_DICT['파우루']:
    skill_manager.apply_function(cooldown_reduction_pauru)
  elif skill_on_use.get_attribute('name') == SKILL_NAME_DICT['마리린']:
    skill_manager.apply_function(cooldown_reduction_maririn)
  elif skill_on_use.get_attribute('name') == SKILL_NAME_DICT['켈시온']:
    skill_manager.apply_function(cooldown_reduction_kelsion)

# 소환수 체인 스킬 사용 후처리, 교감 쿨타임 감소 적용
def use_summon_chain(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 교감 체크
  co_cooldown_reduction = (1 - buff_manager.base_character.cooldown_reduction)
  if buff_manager.is_buff_exists('communication_overflow'):
    co_cooldown_reduction = co_cooldown_reduction * (1 - 0.10)
  # 스킬별 쿨다운
  pauru_cooldown = 8.0 * co_cooldown_reduction
  maririn_cooldown = 12.0 * co_cooldown_reduction
  kelsion_cooldown = 8.0 * co_cooldown_reduction
  # 각 체인 스킬별 스킬 쿨감
  def cooldown_reduction_pauru(skill: Skill):
    if skill.get_attribute('name') == SKILL_NAME_DICT['파우루_체인']:
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(pauru_cooldown))
    return
  def cooldown_reduction_maririn(skill: Skill):
    if skill.get_attribute('name') == SKILL_NAME_DICT['마리린_체인']:
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(maririn_cooldown))
    return
  def cooldown_reduction_kelsion(skill: Skill):
    if skill.get_attribute('name') == SKILL_NAME_DICT['켈시온_체인']:
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(kelsion_cooldown))
    return
  # 소환수 체인 스킬 사용시 다음 체인 스킬 시점에도 소환수가 존재할 경우 체인 스킬 사용가능하게 변경
  current_tick = buff_manager.current_tick
  if (skill_on_use.get_attribute('name') == SKILL_NAME_DICT['파우루_체인'] 
      and buff_manager.is_buff_exists('pauru')
      and not buff_manager.get_buff('pauru').is_expired(current_tick + seconds_to_ticks(pauru_cooldown))):
    skill_manager.apply_function(cooldown_reduction_pauru)
  elif (skill_on_use.get_attribute('name') == SKILL_NAME_DICT['마리린_체인'] 
      and buff_manager.is_buff_exists('maririn')
      and not buff_manager.get_buff('maririn').is_expired(current_tick + seconds_to_ticks(maririn_cooldown))):
    skill_manager.apply_function(cooldown_reduction_maririn)
  elif (skill_on_use.get_attribute('name') == SKILL_NAME_DICT['켈시온_체인'] 
      and buff_manager.is_buff_exists('kelsion')
      and not buff_manager.get_buff('kelsion').is_expired(current_tick + seconds_to_ticks(kelsion_cooldown))):
    skill_manager.apply_function(cooldown_reduction_kelsion)

# 폭풍의 질주 데미지 버프 등록(마력의 질주 1트포)
def activate_stormlike_gallop(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '마력의 질주' and skill_on_use.get_attribute('tripod')[0] == '2':
    buff_manager.register_buff(CLASS_BUFF_DICT['Stormlike_Gallop'], None)

# 파우루 데미지 버프 등록
def activate_pauru(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '파우루':
    if skill_on_use.get_attribute('tripod') == '311' and buff_manager.is_buff_exists('communication_overflow'):
      buff_manager.register_buff(CLASS_BUFF_DICT['Blue_Flame_Pauru_CO'], skill_on_use)
    else:
      raise ValueError

# 엘씨드 데미지 버프 등록
def activate_elcid(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '엘씨드':
    if skill_on_use.get_attribute('tripod') == '212':
      if buff_manager.is_buff_exists('communication_overflow'):
        buff_manager.register_buff(CLASS_BUFF_DICT['Elite_Elcid_CO'], skill_on_use)
      else:
        buff_manager.register_buff(CLASS_BUFF_DICT['Elite_Elcid'], skill_on_use)
    else:
      raise ValueError

# 마리린 데미지 버프 등록
def activate_maririn(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '마리린':
    if skill_on_use.get_attribute('tripod') == '121' and buff_manager.is_buff_exists('communication_overflow'):
      buff_manager.register_buff(CLASS_BUFF_DICT['Maririn_CO'], skill_on_use)
    else:
      raise ValueError

# 슈르디 데미지 버프 등록
def activate_shurdi(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 기본 데미지 추가
  if skill_on_use.get_attribute('name') == '슈르디':
    if skill_on_use.get_attribute('tripod')[1] == '3':
      buff_manager.register_buff(CLASS_BUFF_DICT['Faltering_Shurdi'], skill_on_use)
    elif skill_on_use.get_attribute('tripod')[1] == '1':
      if buff_manager.is_buff_exists('communication_overflow'):
        buff_manager.register_buff(CLASS_BUFF_DICT['Smart_Shurdi_CO'], skill_on_use)
      else:
        raise ValueError
        buff_manager.register_buff(CLASS_BUFF_DICT['Smart_Shurdi'], skill_on_use)
    else:
      raise ValueError
  # 짜릿한 빛 추가
  if skill_on_use.get_attribute('name') == '슈르디' and skill_on_use.get_attribute('tripod')[2] == '1':
    if buff_manager.is_buff_exists('communication_overflow'):
      buff_manager.register_buff(CLASS_BUFF_DICT['Thrilling_Light_CO'], skill_on_use)
    else:
      raise ValueError
      buff_manager.register_buff(CLASS_BUFF_DICT['Thrilling_Light'], skill_on_use)

# 켈시온 데미지 버프 등록
def activate_kelsion(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '켈시온':
    if buff_manager.is_buff_exists('communication_overflow'):
      buff_manager.register_buff(CLASS_BUFF_DICT['Kelsion_CO'], skill_on_use)
    else:
      raise ValueError
      buff_manager.register_buff(CLASS_BUFF_DICT['Kelsion'], skill_on_use)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_ancient_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Ancient':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_ancient_multiplier)

# 상급 소환사 각인
def master_summoner_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if (skill.get_attribute('identity_type') == 'Common' 
      or skill.get_attribute('identity_type') == 'Ancient'):
      s_dm = skill.get_attribute('damage_multiplier')
      s_acr = skill.get_attribute('crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
      skill.update_attribute('crit_rate', s_acr + 0.16)

# 넘치는 교감 각인
def communication_overflow_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if (skill.get_attribute('identity_type') == 'Summon' 
        or skill.get_attribute('name') == '켈시온'
        or skill.get_attribute('name') == SKILL_NAME_DICT['켈시온_체인']):
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.25)

# 슈르디 - 빛의 성장 치적 증가 
def crit_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('crit_rate')
    skill.update_attribute('crit_rate', s_acr + 0.118)

# 이끼늪, 엘시드 공증
def ap_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.444 * (1 + c_aap))

# 방깎 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_adrr = skill.get_attribute('defense_reduction_rate')
    skill.update_attribute('defense_reduction_rate', s_adrr + 0.12)

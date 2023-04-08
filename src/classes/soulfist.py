"""
Actions & Buff bodies of soulfist
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.core.utils import seconds_to_ticks
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 금강선공 증폭 특화 계수
SPEC_COEF_1 = 1 / 46.6 / 100
# 운기조식 시간 감소 특화 계수
SPEC_COEF_2 = 1 / 23.3 / 100
# 금강선공 유지 시간
DEFUALT_HYPE_DURATION_1 = 90
DEFUALT_HYPE_DURATION_2 = 40
DEFUALT_HYPE_DURATION_3 = 20
# 운기조식 시간
DEFAULT_HYPE_COOLDOWN_TIME = 50

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 세맥타통 1레벨
  'Energy_Overflow_1': {
    'name': 'energy_overflow',
    'buff_type': 'stat',
    'effect': 'energy_overflow_1',
    'duration': 999999,
    'priority': 7,
  },
  # 세맥타통 3레벨
  'Energy_Overflow_3': {
    'name': 'energy_overflow',
    'buff_type': 'stat',
    'effect': 'energy_overflow_3',
    'duration': 999999,
    'priority': 7,
  },
  # 역천지체 확인용 버프
  'Robust_Spirit_Enabled_1': {
    'name': 'robust_spirit_enabled_1',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  'Robust_Spirit_Enabled_3': {
    'name': 'robust_spirit_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  # 금강선공 1단계 버프
  'Hype_1': {
    'name': 'hype_1',
    'buff_type': 'stat',
    'effect': 'hype_1',
    'duration': DEFUALT_HYPE_DURATION_1,
    'priority': 9,
  },
  # 금강선공 2단계 버프
  'Hype_2': {
    'name': 'hype_2',
    'buff_type': 'stat',
    'effect': 'hype_2',
    'duration': DEFUALT_HYPE_DURATION_2,
    'priority': 9,
  },
  # 금강선공 3단계 버프
  'Hype_3': {
    'name': 'hype_3',
    'buff_type': 'stat',
    'effect': 'hype_3',
    'duration': DEFUALT_HYPE_DURATION_3,
    'priority': 9,
  },
  # 강화 금강선공 3단계 버프(역천지체 1레벨)
  'Hype_3_RS1': {
    'name': 'hype_3',
    'buff_type': 'stat',
    'effect': 'hype_3_rs3',
    'duration': DEFUALT_HYPE_DURATION_3,
    'priority': 9,
  },
  # 강화 금강선공 3단계 버프(역천지체 3레벨)
  'Hype_3_RS3': {
    'name': 'hype_3',
    'buff_type': 'stat',
    'effect': 'hype_3_rs3',
    'duration': DEFUALT_HYPE_DURATION_3,
    'priority': 9,
  },
  # 내공방출 공증 버프
  'AP_Buff_1': {
    'name': 'AP_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_1',
    'duration': 6,
    'priority': 9,
  },
  # 순보 공증 버프
  'AP_Buff_2': {
    'name': 'AP_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_2',
    'duration': 3,
    'priority': 7,
  },
  # 회선 피증 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 16,
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
  if name == '금강선공 1단계 활성화':
    skill.triggered_actions.append('activate_hype_1')
  elif name == '금강선공 2단계 활성화':
    skill.triggered_actions.append('activate_hype_2')
  elif name == '금강선공 3단계 활성화':
    skill.triggered_actions.append('activate_hype_3')
  elif name == '순보_2회':
    skill.triggered_actions.append('flash_step_action')
  elif name == '순보_3회':
    skill.triggered_actions.append('flash_step_action')
  # apply tripods
  if name == '내공 방출':
    if tripod[2] == '1':
      skill.triggered_actions.append('activate_ap_buff')
  elif name == '회선격추':
    if tripod[1] == '1':
      skill.triggered_actions.append('activate_synergy')
  elif name == '순보_3회':
    if tripod[1] == '3':
      skill.triggered_actions.append('activate_ap_buff')

######## Actions #########
# 피증 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '회선격추':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 내공 방출, 순보 공증 버프 등록
def activate_ap_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '내공 방출':
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_1'], skill_on_use)
  elif skill_on_use.get_attribute('name') == '순보_3회':
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_2'], skill_on_use)
   
# 금강선공 1단계 활성화
def activate_hype_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 금강선공 2,3단계 버프 삭제
  if buff_manager.is_buff_exists('hype_2'):
    buff_manager.unregister_buff('hype_2')
  elif buff_manager.is_buff_exists('hype_3'):
    buff_manager.unregister_buff('hype_3')
  # 금강선공 1단계 버프 등록
  buff_manager.register_buff(CLASS_BUFF_DICT['Hype_1'], skill_on_use)
  # 금강선공 2단계 활성화 쿨타임 초기화
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '금강선공 2단계 활성화':
      skill.update_attribute('remaining_cooldown', 0)
    return
  skill_manager.apply_function(cooldown_reduction)

# 금강선공 2단계 활성화cooldown_reduction_normal
def activate_hype_2(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 금강선공 1,3단계 버프 삭제
  if buff_manager.is_buff_exists('hype_1'):
    buff_manager.unregister_buff('hype_1')
  elif buff_manager.is_buff_exists('hype_3'):
    buff_manager.unregister_buff('hype_3')
  # 금강선공 2단계 버프 등록
  buff_manager.register_buff(CLASS_BUFF_DICT['Hype_2'], skill_on_use)
  # 금강선공 3단계 활성화 쿨타임 초기화
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '금강선공 3단계 활성화':
      skill.update_attribute('remaining_cooldown', 0)
    return
  skill_manager.apply_function(cooldown_reduction)

# 금강선공 3단계 활성화
def activate_hype_3(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  robust_spirit_flag = False
  # 금강선공 1,2단계 버프 삭제
  if buff_manager.is_buff_exists('hype_1'):
    buff_manager.unregister_buff('hype_1')
  elif buff_manager.is_buff_exists('hype_2'):
    buff_manager.unregister_buff('hype_2')
  # 금강선공 3단계 버프 등록
  # 역천지체 각인 존재시 강화 금강선공 버프 등록
  if buff_manager.is_buff_exists('robust_spirit_enabled_1'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Hype_3_RS1'], skill_on_use)
    robust_spirit_flag = True
  elif buff_manager.is_buff_exists('robust_spirit_enabled_3'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Hype_3_RS3'], skill_on_use)
    robust_spirit_flag = True
  # 역천지체 각인 존재하지 않을 시 일반 금강선공 버프 등록
  else:
    buff_manager.register_buff(CLASS_BUFF_DICT['Hype_3'], skill_on_use)
  # 운기조식 적용, 금강선공 1단계 또는 3단계 쿨타임 적용
  c_s = buff_manager.character_specialization
  s_hype_cooldown_reduction_multiplier = (1 - c_s * SPEC_COEF_2)
  def cooldown_reduction_normal(skill: Skill):
    if skill.get_attribute('name') == '금강선공 1단계 활성화':
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(DEFUALT_HYPE_DURATION_3 + DEFAULT_HYPE_COOLDOWN_TIME * s_hype_cooldown_reduction_multiplier))
    return
  def cooldown_reduction_rs(skill: Skill):
    if skill.get_attribute('name') == '금강선공 3단계 활성화':
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(DEFUALT_HYPE_DURATION_3 + DEFAULT_HYPE_COOLDOWN_TIME * s_hype_cooldown_reduction_multiplier))
    return
  # 역천지체시 금강선공 3단계에 쿨감 적용
  if robust_spirit_flag:
    skill_manager.apply_function(cooldown_reduction_rs)
  # 기본시 금강선공 1단계에 쿨감 적용
  else:
    skill_manager.apply_function(cooldown_reduction_normal)

# 순보 쿨감 관리용 액션
def flash_step_action(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  s_rc = skill_on_use.get_attribute("remaining_cooldown")
  # 순보_2회 의 쿨타임을 순보_1회 에도 적용
  if skill_on_use.get_attribute('name') == '순보_2회':
    def cooldown_sync(skill: Skill):
      s_n = skill.get_attribute('name')
      if (s_n == '순보_1회'):
        skill.update_attribute('remaining_cooldown', s_rc)
    skill_manager.apply_function(cooldown_sync)
  # 순보_3회 의 쿨타임을 순보_1회, 순보_2회 에도 적용
  if skill_on_use.get_attribute('name') == '순보_3회':
    def cooldown_sync(skill: Skill):
      s_n = skill.get_attribute('name')
      if (s_n == '순보_1회' or s_n == '순보_2회'):
        skill.update_attribute('remaining_cooldown', s_rc)
    skill_manager.apply_function(cooldown_sync)


######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)

# 금강선공 단계별 버프, 쿨감 먼저 합적용
def hype_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_s = character.get_attribute('specialization')
    s_hype_multiplier = (1 + c_s * SPEC_COEF_1)
    c_cr = character.get_attribute('cooldown_reduction')
    character.update_attribute('cooldown_reduction', c_cr + 0.05 * s_hype_multiplier)
    c_as = character.get_attribute('attack_speed')
    character.update_attribute('attack_speed', c_as + 0.05 * s_hype_multiplier)
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * (1 + 0.10 * s_hype_multiplier))

def hype_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_s = character.get_attribute('specialization')
    s_hype_multiplier = (1 + c_s * SPEC_COEF_1)
    c_cr = character.get_attribute('cooldown_reduction')
    character.update_attribute('cooldown_reduction', c_cr + 0.10 * s_hype_multiplier)
    c_as = character.get_attribute('attack_speed')
    character.update_attribute('attack_speed', c_as + 0.10 * s_hype_multiplier)
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * (1 + 0.25 * s_hype_multiplier))
    
def hype_3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_s = character.get_attribute('specialization')
    s_hype_multiplier = (1 + c_s * SPEC_COEF_1)
    c_cr = character.get_attribute('cooldown_reduction')
    character.update_attribute('cooldown_reduction', c_cr + 0.25 * s_hype_multiplier)
    c_as = character.get_attribute('attack_speed')
    character.update_attribute('attack_speed', c_as + 0.15 * s_hype_multiplier)
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * (1 + 0.60 * s_hype_multiplier))

# 강화 금강선공 3단계(역천지체)
# 역천지체 1레벨
def hype_3_rs1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_s = character.get_attribute('specialization')
    s_hype_multiplier = (1 + c_s * SPEC_COEF_1)
    c_cr = character.get_attribute('cooldown_reduction')
    character.update_attribute('cooldown_reduction', c_cr + 0.25 * s_hype_multiplier)
    c_as = character.get_attribute('attack_speed')
    character.update_attribute('attack_speed', c_as + 0.15 * s_hype_multiplier)
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * (1 + 0.70 * s_hype_multiplier))

# 역천지체 3레벨
def hype_3_rs3(character: CharacterLayer, skill: Skill, buff: Buff):
    c_s = character.get_attribute('specialization')
    s_hype_multiplier = (1 + c_s * SPEC_COEF_1)
    c_cr = character.get_attribute('cooldown_reduction')
    character.update_attribute('cooldown_reduction', c_cr + 0.25 * s_hype_multiplier)
    c_as = character.get_attribute('attack_speed')
    character.update_attribute('attack_speed', c_as + 0.15 * s_hype_multiplier)
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * (1 + 0.90 * s_hype_multiplier))

# 내공 방출 공증 버프
def ap_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.556 * (1 + c_aap))

# 순보 공증 버프
def ap_buff_2(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.444 * (1 + c_aap))

# 피증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)

# 세맥타통 각인
def energy_overflow_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.05)

def energy_overflow_3(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.15)
    


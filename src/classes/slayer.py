"""
Actions & Buff bodies of slayer
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.core.utils import seconds_to_ticks, ticks_to_seconds
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 기본 폭주 지속 시간
DEFAULT_BERSERK_TIME_LIMIT = 30

# 폭주 상태 스킬 피해량 증가 특화 계수
SPEC_COEF_1 = 1 / 69.90 / 100

# 블러드러스트 스킬 피해량 증가 특화 계수
SPEC_COEF_2 = 1 / 5.825 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 처단자 확인용 버프
  'Punisher_Enabled_3': {
    'name': 'punisher_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
   # 포식자 확인용 버프
  'Devourer_Enabled_3': {
    'name': 'devourer_enabled_3',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  # 처단자 버프, 폭주시 같이 켜짐
  'Punisher_3': {
    'name': 'punisher',
    'buff_type': 'stat',
    'effect': 'punisher_3',
    'duration': DEFAULT_BERSERK_TIME_LIMIT * 0.50,
    'priority': 7,
  },
  # 포식자 버프, 폭주시 같이 켜짐
  'Devourer_3': {
    'name': 'devourer',
    'buff_type': 'stat',
    'effect': 'devourer_3',
    'duration': DEFAULT_BERSERK_TIME_LIMIT * 3.00,
    'priority': 7,
  },
  # 폭주 버프
  'Berserk': {
    'name': 'berserk',
    'buff_type': 'stat',
    'effect': 'berserk',
    'duration': DEFAULT_BERSERK_TIME_LIMIT,
    'priority': 7,
  },
  # 플래시 블레이드 피증 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 7,
    'priority': 7,
  },
  # 와일드 스톰프 공속 버프
  'Swift_Attck_Prep': {
    'name': 'swift_attck_prep',
    'buff_type': 'stat',
    'effect': 'swift_attck_prep',
    'duration': 4,
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
  if name == '폭주 활성화':
    skill.triggered_actions.append('activate_berserk')
  # apply tripods
  if name == '와일드 스톰프':
    if tripod[1] == '2':
      skill.triggered_actions.append('activate_swift_attack_prep')
  if name == '플래시 블레이드':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_synergy')
  

######## Actions #########
# 피증 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '플래시 블레이드':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 와일드 스톰프 공속 버프 등록
def activate_swift_attack_prep(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '와일드 스톰프':
    buff_manager.register_buff(CLASS_BUFF_DICT['Swift_Attck_Prep'], skill_on_use)

# 폭주 켜기
def activate_berserk(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  berserk_time = DEFAULT_BERSERK_TIME_LIMIT
  # 포식자 버프 확인 및 등록
  if buff_manager.is_buff_exists('devourer_enabled_3'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Devourer_3'], skill_on_use)
    berserk_time = berserk_time * 3.00
    # 포식자 각인 활성화시 폭주 리필 시간 조정
    def cooldown_increase(skill: Skill):
      if skill.get_attribute('name') == '폭주 활성화':
        skill.update_attribute('remaining_cooldown', seconds_to_ticks(90))
      return
    skill_manager.apply_function(cooldown_increase)
  # 처단자 버프 확인 및 등록
  elif buff_manager.is_buff_exists('punisher_enabled_3'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Punisher_3'], skill_on_use)
    berserk_time = berserk_time / 2.0
  # 폭주 버프 등록
  berserk_dict = CLASS_BUFF_DICT['Berserk'].copy()
  berserk_dict['duration'] = berserk_time
  buff_manager.register_buff(berserk_dict, skill_on_use)
  # 블러드러스트 쿨타임 초기화
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '블러드러스트':
      skill.update_attribute('remaining_cooldown', 0)
    return
  skill_manager.apply_function(cooldown_reduction)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_awakening_multiplier = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_bloody_multiplier = (1 + s * SPEC_COEF_2)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_awakening_multiplier)
    elif skill.get_attribute('name') == '블러드러스트':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_bloody_multiplier)

# 피증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
  s_dm = skill.get_attribute('damage_multiplier')
  skill.update_attribute('damage_multiplier', s_dm * 1.06)

# 폭주 버프
def berserk(character: CharacterLayer, skill: Skill, buff: Buff):
  # 폭주시 뎀증 및 치적 파트
  s = character.get_attribute('specialization')
  s_damage_on_berserk_multiplier = (1 + s * SPEC_COEF_1)
  s_dm = skill.get_attribute('damage_multiplier')
  s_acr = skill.get_attribute('crit_rate')
  skill.update_attribute('damage_multiplier', s_dm * s_damage_on_berserk_multiplier)
  skill.update_attribute('crit_rate', s_acr + 0.30)
  # 공이속 파트
  c_ms = character.get_attribute('movement_speed')
  c_as = character.get_attribute('attack_speed')
  character.update_attribute('attack_speed', c_as + 0.20)
  character.update_attribute('movement_speed', c_ms + 0.20)

# 처단자
def punisher_3(character: CharacterLayer, skill: Skill, buff: Buff):
  # 폭주시 뎀증 파트
  s_dm = skill.get_attribute('damage_multiplier')
  skill.update_attribute('damage_multiplier', s_dm * 1.25)
  # 블러드러스트 치적 증가
  if skill.get_attribute('name') == '블러드러스트':
    s_acr = skill.get_attribute('crit_rate')
    skill.update_attribute('crit_rate', s_acr + 0.20)

# 포식자
def devourer_3(character: CharacterLayer, skill: Skill, buff: Buff):
  # 폭주시 치피증 파트
  s_acd = skill.get_attribute('crit_damage')
  skill.update_attribute('crit_damage', s_acd + 0.40)

# 와일드 스톰프 속공 준비 공속 버프
def swift_attck_prep(character: CharacterLayer, skill: Skill, buff: Buff):
  c_as = character.get_attribute('attack_speed')
  character.update_attribute('attack_speed', c_as + 0.30)

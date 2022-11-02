"""
Actions & Buff bodies of battlemaster
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks, ticks_to_seconds
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 오의 스킬 피해량 증가 특화 계수
SPEC_COEF_1 = 1 / 25.8910 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 용맹의 포효 치적 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 6,
    'priority': 7,
  },
  # 바람의 속삭임 공이속 시너지
  'Synergy_2': {
    'name': 'synergy_2',
    'buff_type': 'stat',
    'effect': 'synergy_2',
    'duration': 6,
    'priority': 7,
  },
  # 바람의 속삭임 공격력 증가 버프
  'AP_Buff_1': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_1',
    'duration': 6,
    'priority': 9,
  },
  # 붕천퇴 공격력 증가 버프
  'AP_Buff_2': {
    'name': 'ap_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_2',
    'duration': 3,
    'priority': 7,
  },
  # 내공연소 틱 데미지 버프, 10멸
  'Energy_Combustion': {
    'name': 'energy_combustion',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 332,
    'coefficient': 3.6787 * 1.4,
    'damage_interval': 1,
    'duration': 20,
    'priority': 7,
  },
  # 내공연소 최후의 속삭임 데미지, 10멸
  'Last_Whisper': {
    'name': 'last_whisper',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 3523,
    'coefficient': 58.1024 * 1.4,
    'damage_interval': 1,
    'duration': 1,
    'priority': 7,
  },
  # 월섬각 강렬한 전격 데미지, 10멸
  'Intense_Shock': {
    'name': 'intense_shock',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 271,
    'coefficient': 1.68 * 1.4,
    'damage_interval': 1,
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
  if name == '내공연소':
    skill.triggered_actions.append('activate_energy_combustion')
  # apply tripods
  if name == '붕천퇴':
    if tripod[1] == '3':
      skill.triggered_actions.append('activate_ap_buff')
  elif name == '월섬각':
    if tripod[0] == '2':
      skill.triggered_actions.append('activate_damage_buff')
  elif name == '바람의 속삭임':
    skill.triggered_actions.append('activate_synergy')
    if tripod[2] == '1':
      skill.triggered_actions.append('activate_ap_buff')
  elif name == '용맹의 포효':
    skill.triggered_actions.append('activate_synergy')
  elif name == '내공연소':
    skill.triggered_actions.append('activate_damage_buff')

######## Actions #########
# 치적 및 공이속 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '용맹의 포효':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')
  elif skill_on_use.get_attribute('name') == '바람의 속삭임':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_2'], 'class')

# 공격력 증가 버프 등록 action
def activate_ap_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '바람의 속삭임':
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_1'], 'class')
  elif skill_on_use.get_attribute('name') == '붕천퇴':
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_2'], 'class')
  
# 데미지 버프 등록 action
def activate_damage_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '월섬각':
    buff_manager.register_buff(CLASS_BUFF_DICT['Intense_Shock'], 'class')
  elif skill_on_use.get_attribute('name') == '내공연소':
    buff_manager.register_buff(CLASS_BUFF_DICT['Last_Whisper'], 'class')

# 내공연소 기본 틱 데미지 버프 등록 action
def activate_energy_combustion(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Energy_Combustion'], 'class')
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '내공연소 버프 체크':
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(20))
  skill_manager.apply_function(cooldown_reduction)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    eso_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Esoteric':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * eso_multiplier)

# 용포 치적 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
  s_acr = skill.get_attribute('additional_crit_rate')
  skill.update_attribute('additional_crit_rate', s_acr + 0.18)

# 바속 공이속 시너지
def synergy_2(character: CharacterLayer, skill: Skill, buff: Buff):
  c_as = character.get_attribute('attack_speed')
  c_ms = character.get_attribute('movement_speed')
  character.update_attribute('attack_speed', c_as + 0.08)
  character.update_attribute('movement_speed', c_ms + 0.16)

# 바속 공증 버프
def ap_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
  c_aap = character.get_attribute('additional_attack_power')
  character.update_attribute('additional_attack_power', c_aap + 0.497 * (1 + c_aap))

# 붕천퇴 공증 버프
def ap_buff_2(character: CharacterLayer, skill: Skill, buff: Buff):
  c_aap = character.get_attribute('additional_attack_power')
  character.update_attribute('additional_attack_power', c_aap + 0.276 * (1 + c_aap))

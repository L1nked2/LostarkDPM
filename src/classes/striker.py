"""
Actions & Buff bodies of striker
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.core.utils import seconds_to_ticks
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 오의 뎀증 특화 계수
SPEC_COEF_1 = 0.225 / 699

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  # 일격필살 버프
  'Deathblow_3': {
    'name': 'deathblow',
    'buff_type': 'stat',
    'effect': 'deathblow',
    'duration': 999999,
    'priority': 7,
  }, 
  # 오의난무 버프
  'Esoteric_Flurry_3': {
    'name': 'esoteric_flurry',
    'buff_type': 'stat',
    'effect': 'esoteric_flurry',
    'duration': 999999,
    'priority': 7,
  },
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 6,
    'priority': 7,
  },
  'Speed_Buff_1': {
    'name': 'speed_buff',
    'buff_type': 'stat',
    'effect': 'speed_buff_1',
    'duration': 4,
    'priority': 7,
  },
  # 화염 폭발(5렙), 보석 적용x
  'Flame_Explosion': {
    'name': 'flame_explosion',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 248,
    'coefficient': 9.06,
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
  if name == '번개의 속삭임':
    skill.triggered_actions.append('activate_synergy')
  # apply tripods
  if name == '붕천퇴':
    if tripod[1] == '3':
      skill.triggered_actions.append('activate_speed_buff')
  if name == '나선경':
    if tripod[2] == '3'
      skill.triggered_actions.append('activate_speed_buff')
  elif name == '폭쇄진':
    if tripod[1] == '3':
      skill.triggered_actions.append('action_1')

######## Actions #########

# 번개의 속삭임 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 붕천퇴 공이속 버프 등록
def activate_speed_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Speed_Buff_1'], skill_on_use)

# 폭쇄진 2트포 화염 폭발 action
def action_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Flame_Explosion'], None)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_multiplier_2 = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Esoteric':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_2)

# 번개의 속삭임 치적 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('crit_rate')
    skill.update_attribute('crit_rate', s_acr + 0.18)

# 붕천퇴/나선경 공이속 버프
def speed_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.192)
    character.update_attribute('movement_speed', c_ms + 0.192)

# 일격필살 버프
def deathblow(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Esoteric':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.7)
      
# 오의난무 버프
def esoteric_flurry(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Esoteric':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.3)
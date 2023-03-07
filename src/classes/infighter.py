"""
Actions & Buff bodies of infighter(scrapper)
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 충격 뎀증 특화 계수
SPEC_COEF_1 = 1 / 17.475 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Shock_Training_3': {
    'name': 'shock_training',
    'buff_type': 'stat',
    'effect': 'shock_training_3',
    'duration': 999999,
    'priority': 7,
  },
  'Taijutsu_3': {
    'name': 'taijutsu',
    'buff_type': 'stat',
    'effect': 'taijutsu_3',
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
  # 화신출격(5렙)
  'Conflagration_Attack': {
    'name': 'conflagration_attack',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 309,
    'coefficient': 1.91,
    'damage_interval': 1,
    'duration': 6,
    'priority': 7,
  },
  # 불굴의 힘(1렙), 보석 적용x
  'Undying_Power': {
    'name': 'undying_power',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 67,
    'coefficient': 0.4,
    'damage_interval': 5,
    'duration': 6,
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
  if (name == '용의 강림' and tripod[1] == '2') and rune[:2] =='출혈':
    skill.triggered_actions.append('extend_bleed')
  # apply tripods
  if name == '맹호격':
    if tripod[0] == '2':
      skill.triggered_actions.append('activate_synergy')
  elif name == '파쇄의 강타_1타':
    if tripod[0] == '3':
      skill.triggered_actions.append('activate_synergy')
  elif name == '일망 타진':
    if tripod[0] == '1':
      skill.triggered_actions.append('swift_preparation')
  elif name == '용의 강림':
    if tripod[1] == '2':
      skill.triggered_actions.append('action_1')
  elif name == '지진쇄':
    if tripod[0] == '2':
      skill.triggered_actions.append('action_2')

######## Actions #########
# 맹호격, 파쇄의 강타 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 일망 타진 쿨초
def swift_preparation(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '일망 타진':
      skill.update_attribute('remaining_cooldown', 0)
    return
  if skill_manager.check_chance((1 - 0.54 * 0.54), 'swift_preperation'):
    skill_manager.apply_function(cooldown_reduction)

# 용의 강림 출혈 갱신
def extend_bleed(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def duration_increase(buff: Buff):
    if buff.name == '출혈':
      buff.duration += seconds_to_ticks(6)
  buff_manager.apply_function(duration_increase)

# 용의 강림 2트포 등록 action
def action_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Conflagration_Attack'], skill_on_use)

# 지진쇄 1트포 action
def action_2(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Undying_Power'], None)

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_multiplier_2 = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Shock':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_2)

# 맹호격, 파쇄의 강타 뎀증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)

# 충격 단련 버프
def shock_training_3(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Shock':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.2)

# 극의 : 체술 버프
def taijutsu_3(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Stamina':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.65)
  elif skill.get_attribute('identity_type') == 'Shock':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 0.7)


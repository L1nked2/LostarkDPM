"""
Actions & Buff bodies of infighter(scrapper)
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 충격 뎀증 특화 계수
SPEC_COEF_1 = 1 / 17.5355 / 100

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
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 8,
    'priority': 7,
  },
}

# Actions
# 맹호격, 파쇄의 강타 시너지 등록
def activate_synergy_1(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

def swift_preparation(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '일망타진':
      skill.update_attribute('remaining_cooldown', seconds_to_ticks(1))
    return
  if check_chance(0.75):
    skill_manager.apply_function(cooldown_reduction)

# Buff bodies
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

# 일격필살 버프
def shock_training_3(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Shock':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.2)
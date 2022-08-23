"""
Actions & Buff bodies of blaster
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 포격 스킬 피해량 특화 계수
SPEC_COEF_1 = 1 / 13.9806 / 100
# 화력 버프 효율 특화 계수
SPEC_COEF_2 = 1 / 11.2746 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Firepower_Enhancement_3': {
    'name': 'firepower_enhancement',
    'buff_type': 'stat',
    'effect': 'firepower_enhancement_3',
    'duration': 999999,
    'priority': 7,
  },
  'Barrage_Enhancement_3': {
    'name': 'barrage_enhancement',
    'buff_type': 'stat',
    'effect': 'barrage_enhancement_3',
    'duration': 999999,
    'priority': 7,
  },
  # 강화탄 방깎 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 8,
    'priority': 7,
  },
  # 화염 폭격 데미지 버프, 3중첩
  'Flame_Barrage': {
    'name': 'flame_barrage',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 429,
    'coefficient': 2.7,
    'damage_interval': 1,
    'duration': 5,
    'priority': 7,
  },
}

# Actions
# 포탑 출혈 시간 갱신 action
def extend_bleed(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def duration_increase(buff: Buff):
    if buff.name == 'bleed':
      buff.duration += seconds_to_ticks(13)
  buff_manager.apply_function(duration_increase)

# 방깎 시너지 등록
def activate_synergy_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 화염 폭격 데미지 버프 등록
def activate_flame_barrage(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Flame_Barrage'], 'class')

# Buff bodies
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_barrage_multiplier = (1 + s * SPEC_COEF_1)
    s_firepower_buff_multiplier = (1 + s * SPEC_COEF_2)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == "Barrage":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_barrage_multiplier)
    # 화력 게이지 상시 풀 유지
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * (1 + (0.30 * s_firepower_buff_multiplier)))

def firepower_enhancement_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('identity_type') == 'Common':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.20)

def barrage_enhancement_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('identity_type') == 'Barrage':
      s_dm = skill.get_attribute('damage_multiplier')
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.20)
      skill.update_attribute('additional_crit_rate', s_acr + 0.40)

# 방깎 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.066)

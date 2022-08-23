"""
Actions & Buff bodies of striker
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION

# 오의 뎀증 특화 계수
SPEC_COEF_1 = 1 / 31.0975 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Esoteric_Prepared_4': {
    'name': 'esoteric_prepared',
    'buff_type': 'stat',
    'effect': 'esoteric_prepared_4',
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
  # 화염 폭발(5렙)
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

######## Actions #########
# 통합 액션
def default_action(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  pass

# 버블 활성화
def prepare_esoteric(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if not buff_manager.is_buff_exists('esoteric_prepared'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Esoteric_Prepared_4'], 'class')

# 버블 사용
def esoteric_used(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.unregister_buff('esoteric_prepared')

# 번개의 속삭임 시너지 등록
def activate_synergy_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 붕천퇴 공이속 버프 등록
def activate_speed_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Speed_Buff_1'], 'class')

# 폭쇄진 2트포 화염 폭발 action
def action_1(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Flame_Explosion'], 'class')

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
    s_acr = skill.get_attribute('additional_crit_rate')
    skill.update_attribute('additional_crit_rate', s_acr + 0.18)

# 붕천퇴 공이속 버프
def speed_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.192)
    character.update_attribute('movement_speed', c_ms + 0.192)

# 일격필살 버프
def esoteric_prepared_4(character: CharacterLayer, skill: Skill, buff: Buff):
  if skill.get_attribute('identity_type') == 'Esoteric':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.7)
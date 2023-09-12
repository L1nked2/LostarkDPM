"""
Actions & Buff bodies of blaster
"""
from src.layers.dynamic import skill
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.core.utils import seconds_to_ticks
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 포격 스킬 피해량 특화 계수
SPEC_COEF_1 = 0.49 / 699
# 화력 버프 효율 특화 계수
SPEC_COEF_2 = 0.58 / 699

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
  # 헤비터렛(각성기, 20초)
  'Heavy_Turret': {
    'name': 'heavy_turret',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 3271.75,
    'coefficient': 20.28485,
    'damage_interval': 1,
    'duration': 20,
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
  if ((name == '포탑 소환') or name == '강화탄' and tripod[2] == '2') and rune[:2] =='출혈':
    skill.triggered_actions.append('extend_bleed')
  if name == '포격 모드 활성화':
    skill.triggered_actions.append('activate_barrage_mode')
  if name == '포격 모드 해제':
    skill.triggered_actions.append('deactivate_barrage_mode')
  if name == '헤비 터렛':
    skill.triggered_actions.append('activate_heavy_turret')
  # apply tripods
  if name == '강화탄':
    if tripod[0] == '1':
      skill.triggered_actions.append('activate_synergy')
  elif name == '공중 폭격':
    if tripod[1] == '1':
      skill.triggered_actions.append('activate_flame_barrage')


######## Actions #########
# 포탑, 강화탄 출혈 시간 갱신 action
def extend_bleed(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 포탑 소환
  if skill_on_use.get_attribute('name') == '포탑 소환':
    def duration_increase(buff: Buff):
      if buff.name == '출혈':
        buff.duration += seconds_to_ticks(13)
    buff_manager.apply_function(duration_increase)
  # 강화탄
  elif skill_on_use.get_attribute('name') == '강화탄':
    def duration_increase(buff: Buff):
      if buff.name == '출혈':
        buff.duration += seconds_to_ticks(4)
    buff_manager.apply_function(duration_increase)

# 포격 모드 활성화
def activate_barrage_mode(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if (skill.get_attribute('name') == '포격 모드 해제' 
        or skill.get_attribute('identity_type') == 'Barrage'):
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 포격 모드 해제
def deactivate_barrage_mode(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '포격 모드 활성화':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 강화탄 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], skill_on_use)

# 화염 폭격 데미지 버프 등록(공폭 2트포)
def activate_flame_barrage(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '공중 폭격' and skill_on_use.get_attribute('tripod')[1] == '1':
    buff_manager.register_buff(CLASS_BUFF_DICT['Flame_Barrage'], None)

# 헤비 터렛 데미지 버프 등록(각성기, 2각)
def activate_heavy_turret(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '헤비 터렛':
    buff_manager.register_buff(CLASS_BUFF_DICT['Heavy_Turret'], skill_on_use)

######## Buff bodies ########
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
      skill.update_attribute('damage_multiplier', s_dm * 1.28)

def barrage_enhancement_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('identity_type') == 'Barrage':
      s_dm = skill.get_attribute('damage_multiplier')
      s_acr = skill.get_attribute('crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.20)
      skill.update_attribute('crit_rate', s_acr + 0.40)

# 방깎 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_adrr = skill.get_attribute('defense_reduction_rate')
    skill.update_attribute('defense_reduction_rate', s_adrr + 0.12)

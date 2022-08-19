"""
Actions & Buff bodies of scouter
"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.utils import check_chance
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 싱크 스킬 피해량 특화 계수
SPEC_COEF_1 = 1 / 11.2781 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Evolutionary_Legacy_Enabled_1': {
    'name': 'evolutionary_legacy_enabled_1',
    'buff_type': 'stat',
    'effect': None,
    'duration': 999999,
    'priority': 7,
  },
  'Arthetinean_Skill_1': {
    'name': 'arthetinean_skill',
    'buff_type': 'stat',
    'effect': 'arthetinean_skill_1',
    'duration': 999999,
    'priority': 9,
  },
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 999999,
    'priority': 7,
  },
  'Synergy_2': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 14,
    'priority': 7,
  },
  'Agility': {
    'name': 'agility',
    'buff_type': 'stat',
    'effect': 'agility',
    'duration': 6,
    'priority': 9,
  },
  'Hyper_Sync': {
    'name': 'hyper_sync',
    'buff_type': 'stat',
    'effect': 'hyper_sync',
    'duration': 999999,
    'priority': 7,
  },
  'Evolutionary_Legacy_1': {
    'name': 'evolutionary_legacy',
    'buff_type': 'stat',
    'effect': 'evolutionary_legacy_1',
    'duration': 6,
    'priority': 7,
  },
  'Flame_Buster': {
    'name': 'flame_buster',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 29,
    'coefficient': 0.19,
    'damage_interval': 1,
    'duration': 5,
    'priority': 7,
  }
}

# Actions
# 하이퍼 싱크 변신 사용 가능 전환
def grant_hyper_sync(buff_manager: BuffManager, skill_manager: SkillManager):
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '하이퍼 싱크 변신':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 하이퍼 싱크 사용
def activate_hyper_sync(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Hyper_Sync'], 'class')
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
  def cooldown_reduction(skill: Skill):
    if skill.get_attribute('name') == '하이퍼 싱크 변신해제':
      skill.update_attribute('remaining_cooldown', 0)
  skill_manager.apply_function(cooldown_reduction)

# 변신 해제
def deactivate_hyper_sync(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.unregister_buff('hyper_sync')
  buff_manager.unregister_buff('evolutionary_legacy')
  buff_manager.unregister_buff('synergy_1')

# 변신시 시너지 등록
def activate_synergy_1(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 과충전 배터리 시너지 등록
def activate_synergy_2(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_2'], 'class')

# 기동 타격 버프 등록
def agility_action(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Agility'], 'class')

# 플레임 버스터 데미지 버프 등록
def activate_flame_buster(buff_manager: BuffManager, skill_manager: SkillManager):
  buff_manager.register_buff(CLASS_BUFF_DICT['Flame_Buster'], 'class')

# 진화의 유산 쿨감 및 버프 스택, 각 스킬별로 제공
def evolutionary_legacy_action_q(buff_manager: BuffManager, skill_manager: SkillManager):
  # 현재 사용한 스킬 제외 쿨감 함수
  def cooldown_reduction(skill: Skill):
    if (skill.get_attribute('identity_type') == 'Sync' 
      and not(skill.get_attribute('name') == "코멧 스트라이크")):
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(0.5))
  # 유산 버프 스택 증가함수
  def increase_legacy_buff_stack(buff: Buff):
    if buff.name == 'evolutionary_legacy' and buff.stack < 3:
      buff.increase_stack()
  # 유산 버프 확인
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    # 유산 버프 갱신 후 쿨감 및 스택증가 적용
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
    buff_manager.apply_function(increase_legacy_buff_stack)
    skill_manager.apply_function(cooldown_reduction)
    
def evolutionary_legacy_action_w(buff_manager: BuffManager, skill_manager: SkillManager):
  # 현재 사용한 스킬 제외 쿨감 함수
  def cooldown_reduction(skill: Skill):
    if (skill.get_attribute('identity_type') == 'Sync' 
      and not(skill.get_attribute('name') == "슬러그 샷")):
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(0.5))
  # 유산 버프 스택 증가함수
  def increase_legacy_buff_stack(buff: Buff):
    if buff.name == 'evolutionary_legacy' and buff.stack < 3:
      buff.increase_stack()
  # 유산 버프 확인
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    # 유산 버프 갱신 후 쿨감 및 스택증가 적용
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
    buff_manager.apply_function(increase_legacy_buff_stack)
    skill_manager.apply_function(cooldown_reduction)

def evolutionary_legacy_action_e(buff_manager: BuffManager, skill_manager: SkillManager):
  # 현재 사용한 스킬 제외 쿨감 함수
  def cooldown_reduction(skill: Skill):
    if (skill.get_attribute('identity_type') == 'Sync' 
      and not(skill.get_attribute('name') == "레이저 블레이드")):
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(0.5))
  # 유산 버프 스택 증가함수
  def increase_legacy_buff_stack(buff: Buff):
    if buff.name == 'evolutionary_legacy' and buff.stack < 3:
      buff.increase_stack()
  # 유산 버프 확인
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    # 유산 버프 갱신 후 쿨감 및 스택증가 적용
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
    buff_manager.apply_function(increase_legacy_buff_stack)
    skill_manager.apply_function(cooldown_reduction)

def evolutionary_legacy_action_r(buff_manager: BuffManager, skill_manager: SkillManager):
  # 현재 사용한 스킬 제외 쿨감 함수
  def cooldown_reduction(skill: Skill):
    if (skill.get_attribute('identity_type') == 'Sync' 
      and not(skill.get_attribute('name') == "엑셀리온 빔")):
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(0.5))
  # 유산 버프 스택 증가함수
  def increase_legacy_buff_stack(buff: Buff):
    if buff.name == 'evolutionary_legacy' and buff.stack < 3:
      buff.increase_stack()
  # 유산 버프 확인
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    # 유산 버프 갱신 후 쿨감 및 스택증가 적용
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
    buff_manager.apply_function(increase_legacy_buff_stack)
    skill_manager.apply_function(cooldown_reduction)

def evolutionary_legacy_action_a(buff_manager: BuffManager, skill_manager: SkillManager):
  # 현재 사용한 스킬 제외 쿨감 함수
  def cooldown_reduction(skill: Skill):
    if (skill.get_attribute('identity_type') == 'Sync' 
      and not(skill.get_attribute('name') == "버스트 블로우")):
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(0.5))
  # 유산 버프 스택 증가함수
  def increase_legacy_buff_stack(buff: Buff):
    if buff.name == 'evolutionary_legacy' and buff.stack < 3:
      buff.increase_stack()
  # 유산 버프 확인
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    # 유산 버프 갱신 후 쿨감 및 스택증가 적용
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
    buff_manager.apply_function(increase_legacy_buff_stack)
    skill_manager.apply_function(cooldown_reduction)

def evolutionary_legacy_action_s(buff_manager: BuffManager, skill_manager: SkillManager):
  # 현재 사용한 스킬 제외 쿨감 함수
  def cooldown_reduction(skill: Skill):
    if (skill.get_attribute('identity_type') == 'Sync' 
      and not(skill.get_attribute('name') == "크림슨 브레이커")):
      rc = skill.get_attribute('remaining_cooldown')
      skill.update_attribute('remaining_cooldown', rc - seconds_to_ticks(0.5))
  # 유산 버프 스택 증가함수
  def increase_legacy_buff_stack(buff: Buff):
    if buff.name == 'evolutionary_legacy' and buff.stack < 3:
      buff.increase_stack()
  # 유산 버프 확인
  if buff_manager.is_buff_exists('evolutionary_legacy_enabled_1'):
    # 유산 버프 갱신 후 쿨감 및 스택증가 적용
    buff_manager.register_buff(CLASS_BUFF_DICT['Evolutionary_Legacy_1'], 'class')
    buff_manager.apply_function(increase_legacy_buff_stack)
    skill_manager.apply_function(cooldown_reduction)

# Buff bodies
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_sync_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == "Sync":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_sync_multiplier)

# 하이퍼 싱크 변신 버프
def hyper_sync(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.15)
    character.update_attribute('movement_speed', c_ms + 0.30)

# 진화의 유산 스택형 버프
def evolutionary_legacy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    if skill.get_attribute('identity_type') == "Sync":
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * (1 + (0.02 * buff.stack)))

# 아르데타인의 기술 버프
def arthetinean_skill_1(character: CharacterLayer, skill: Skill, buff: Buff):
    # 재장전 풀스택 제공
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.05)
    character.update_attribute('movement_speed', c_ms + 0.05)
    # 드론, 합작 스킬 피증
    if (skill.get_attribute('identity_type') == "Drone" 
        or skill.get_attribute('identity_type') == "Joint"):
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.15)

# 공증 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.06)

# 기동 타격 날렵함 버프
def agility(character: CharacterLayer, skill: Skill, buff: Buff):
    c_as = character.get_attribute('attack_speed')
    c_ms = character.get_attribute('movement_speed')
    character.update_attribute('attack_speed', c_as + 0.192)
    character.update_attribute('movement_speed', c_ms + 0.192)



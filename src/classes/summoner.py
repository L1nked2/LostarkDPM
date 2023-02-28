"""
Actions & Buff bodies of Summoner
"""
from src.layers.dynamic import skill
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buff_manager import BuffManager
from src.layers.dynamic.skill_manager import SkillManager
from src.layers.dynamic.skill import Skill
from src.layers.dynamic.buff import Buff
from src.layers.dynamic.constants import seconds_to_ticks
from src.layers.static.constants import AWAKENING_DAMAGE_PER_SPECIALIZATION


# 고대 정령 스킬 피해량 특화 계수
SPEC_COEF_1 = 1 / 8.2235 / 100

CLASS_BUFF_DICT = {
  'Specialization': {
    'name': 'specialization',
    'buff_type': 'stat',
    'effect': 'specialization',
    'duration': 999999,
    'priority': 7,
  },
  'Master_Summoner_3': {
    'name': 'master_summoner',
    'buff_type': 'stat',
    'effect': 'master_summoner_3',
    'duration': 999999,
    'priority': 7,
  },
  # 이끼늪 방깎 시너지
  'Synergy_1': {
    'name': 'synergy_1',
    'buff_type': 'stat',
    'effect': 'synergy_1',
    'duration': 16,
    'priority': 7,
  },
  # 이끼늪, 엘씨드 공증 버프
  'AP_Buff_1': {
    'name': 'AP_buff',
    'buff_type': 'stat',
    'effect': 'ap_buff_1',
    'duration': 5,
    'priority': 7,
  },
  # 슈르디 치적 버프
  'Crit_Buff_1': {
    'name': 'crit_buff',
    'buff_type': 'stat',
    'effect': 'crit_buff_1',
    'duration': 28,
    'priority': 7,
  },
  # 폭풍의 질주 데미지 버프, 멸화x
  'Stormlike_Gallop': {
    'name': 'stormlike_gallop',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 12,
    'coefficient': 0.0222,
    'damage_interval': 1,
    'duration': 5,
    'priority': 7,
  },
  # 엘씨드 데미지 버프, 멸화x
  'Elite_Elcid': {
    'name': 'elite_elcid',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 142,
    'coefficient': 5.08816,
    'damage_interval': 1,
    'duration': 10,
    'priority': 7,
  },
  # 슈르디(허영이) 데미지 버프, 멸화x
  'Faltering_Shurdi': {
    'name': 'faltering_shurdi',
    'buff_type': 'damage',
    'effect': None,
    'base_damage': 514,
    'coefficient': 1.0243018,
    'damage_interval': 1,
    'duration': 28,
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
  if name == '슈르디' and rune[:2] =='출혈':
    skill.triggered_actions.append('extend_bleed')
  # apply tripods
  if name == '끈적이는 이끼늪':
    if tripod[0] == '3':
      skill.triggered_actions.append('activate_ap_buff')
    elif tripod[1] == '1':
      skill.triggered_actions.append('activate_synergy')
  elif name == '마력의 질주':
    if tripod[0] == '2':
      skill.triggered_actions.append('activate_stormlike_gallop')
  elif name == '엘씨드':
    skill.triggered_actions.append('activate_elcid')
    if tripod[0] == '2':
      skill.triggered_actions.append('activate_ap_buff')
  elif name == '슈르디':
    if tripod[0] == '3':
      skill.triggered_actions.append('activate_crit_buff')
    if tripod[1] == '3':
      skill.triggered_actions.append('activate_faltering_shurdi')


######## Actions #########
# 슈르디 출혈 시간 갱신 action
def extend_bleed(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  # 슈르디
  if skill_on_use.get_attribute('name') == '슈르디':
    def duration_increase(buff: Buff):
      if buff.name == '출혈':
        buff.duration += seconds_to_ticks(20)
    buff_manager.apply_function(duration_increase)

# 이끼늪 시너지 등록
def activate_synergy(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '끈적이는 이끼늪' and skill_on_use.get_attribute('tripod')[1] == '1':
    buff_manager.register_buff(CLASS_BUFF_DICT['Synergy_1'], 'class')

# 이끼늪, 엘씨드 공증 등록
def activate_ap_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if ((skill_on_use.get_attribute('name') == '끈적이는 이끼늪'and skill_on_use.get_attribute('tripod')[0] == '3')
    or (skill_on_use.get_attribute('name') == '엘씨드'and skill_on_use.get_attribute('tripod')[0] == '2')):
    buff_manager.register_buff(CLASS_BUFF_DICT['AP_Buff_1'], 'class')

# 슈르디 - 빛의 성장 치적 버프 등록
def activate_crit_buff(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '슈르디' and skill_on_use.get_attribute('tripod')[1] == '3':
    buff_manager.register_buff(CLASS_BUFF_DICT['Crit_Buff_1'], 'class')

# 폭풍의 질주 데미지 버프 등록(마력의 질주 1트포)
def activate_stormlike_gallop(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '마력의 질주' and skill_on_use.get_attribute('tripod')[0] == '2':
    buff_manager.register_buff(CLASS_BUFF_DICT['Stormlike_Gallop'], 'class')

# 엘시드 데미지 버프 등록
def activate_elcid(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '엘씨드' and skill_on_use.get_attribute('tripod')[2] == '2':
    buff_manager.register_buff(CLASS_BUFF_DICT['Elite_Elcid'], 'class')

# 슈르디 데미지 버프 등록
def activate_faltering_shurdi(buff_manager: BuffManager, skill_manager: SkillManager, skill_on_use: Skill):
  if skill_on_use.get_attribute('name') == '슈르디' and skill_on_use.get_attribute('tripod')[1] == '3':
    buff_manager.register_buff(CLASS_BUFF_DICT['Faltering_Shurdi'], 'class')

######## Buff bodies ########
def specialization(character: CharacterLayer, skill: Skill, buff: Buff):
    s = character.get_attribute('specialization')
    s_multiplier_1 = (1 + s * AWAKENING_DAMAGE_PER_SPECIALIZATION)
    s_ancient_multiplier = (1 + s * SPEC_COEF_1)
    if skill.get_attribute('identity_type') == 'Awakening':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_multiplier_1)
    elif skill.get_attribute('identity_type') == 'Ancient':
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * s_ancient_multiplier)

# 상급 소환사 각인
def master_summoner_3(character: CharacterLayer, skill: Skill, buff: Buff):
    if (skill.get_attribute('identity_type') == 'Common' 
      or skill.get_attribute('identity_type') == 'Ancient'):
      s_dm = skill.get_attribute('damage_multiplier')
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.12)
      skill.update_attribute('additional_crit_rate', s_acr + 0.16)

# 슈르디 - 빛의 성장 치적 증가 
def crit_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_acr = skill.get_attribute('additional_crit_rate')
    skill.update_attribute('additional_crit_rate', s_acr + 0.118)

# 이끼늪, 엘시드 공증
def ap_buff_1(character: CharacterLayer, skill: Skill, buff: Buff):
    c_aap = character.get_attribute('additional_attack_power')
    character.update_attribute('additional_attack_power', c_aap + 0.444 * (1 + c_aap))

# 방깎 시너지
def synergy_1(character: CharacterLayer, skill: Skill, buff: Buff):
    s_dm = skill.get_attribute('damage_multiplier')
    skill.update_attribute('damage_multiplier', s_dm * 1.066)

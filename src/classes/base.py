"""

"""
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.skill import Skill

BASE_BUFF_DICT = {
  'Head_Attack': {
    'name': 'head_attack',
    'buff_type': 'stat',
    'duration': 999999,
    'priority': 7,
  },
  'Back_Attack': {
    'name': 'back_attack',
    'buff_type': 'stat',
    'duration': 999999,
    'priority': 7,
  },
}

COMMON_BUFF_DICT = {
  ###### stat buffs ######
  'Raid_Captain_3': {
    'name': 'raid_captain',
    'buff_type': 'stat',
    'duration': 99999999,
    'priority': 7,
  },
  ###### skill buffs ######
  'Super_Charge_3': {
    'name': 'super_charge',
    'buff_type': 'stat',
    'duration': 99999999,
    'priority': 7,
  },
  'Master_Brawler_3': {
    'name': 'master_brawler',
    'buff_type': 'stat',
    'duration': 99999999,
    'priority': 7,
  },
}

# Buff Bodies
# System-based buffs
def head_attack(character: CharacterLayer, skill: Skill):
    if skill.get_attribute('head_attack') == True:
      s_dm = skill.get_attribute('damage_multiplier')
      skill.update_attribute('damage_multiplier', s_dm * 1.2)

def back_attack(character: CharacterLayer, skill: Skill):
    if skill.get_attribute('back_attack') == True:
      s_dm = skill.get_attribute('damage_multiplier')
      s_acr = skill.get_attribute('additional_crit_rate')
      skill.update_attribute('damage_multiplier', s_dm * 1.05)
      skill.update_attribute('additional_crit_rate', s_acr + 0.10)

# Engraving buffs
def raid_captain_3(character: CharacterLayer, skill: Skill):
    c_dm = character.get_attribute('damage_multiplier')
    c_ams = character.get_attribute('actual_movement_speed')
    character.update_attribute('damage_multiplier', c_dm * (1+(c_ams-1)*0.45))

def super_charge_3(character: CharacterLayer, skill: Skill):
    if skill.get_attribute('skill_type') == 'Charge':
      s_dm = skill.get_attribute('damage_multiplier')
      s_tsd = skill.get_attribute('type_specific_delay')
      skill.update_attribute('damage_multiplier', s_dm * 1.20)
      skill.update_attribute('type_specific_delay', s_tsd / 1.40)

def master_brawler_3(character: CharacterLayer, skill: Skill):
    if skill.get_attribute('head_attack') == True:
      s_dm = skill.get_attribute('damage_multiplier')    
      skill.update_attribute('damage_multiplier', s_dm * 1.25)

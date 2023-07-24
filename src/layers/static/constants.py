"""
Constants for static part of simulator
"""

# Data for character_layer
# Combat Stats Related
CRITICAL_RATE_PER_CRIT = 0.2501 / 699
AWAKENING_DAMAGE_PER_SPECIALIZATION = 0.382 / 699
COOLDOWN_REDUCTION_PER_SWIFTNESS = 0.1501 / 699
ATTACK_SPEED_PER_SWIFTNESS = 0.12 / 699
MOVEMENT_SPEED_PER_SWIFTNESS = 0.12 / 699
DEFAULT_DEFENSE = 6500
DEFENSE_CORRECTION = 0.8

# Capping
MAX_MOVEMENT_SPEED = 1.4
MAX_ATTACK_SPEED = 1.4
MAX_COOLDOWN_REDUCTION = 0.8


# Data for engraving_layer
# Static Engravings
# TODO: move all to base.py and each {class}.py, care duplicated buffs
ENGRAVINGS = {
  ####### Helper각인 #######
  #헬모드
  'Hell': [('additional_damage', lambda x: x - 0.30)],
  'Synergy_Crit_A': [('crit_rate', lambda x: x + 0.10)],
  'Synergy_Crit_B': [('crit_rate', lambda x: x + 0.18)],
  'Synergy_Damage': [('character_damage_multiplier', lambda x: x * 1.06)],
  'Synergy_Defense_Reduction': [('static_buff_queue', lambda x: x + ['Synergy_Defense_Reduction'])],
  'Synergy_Head_Back': [('static_buff_queue', lambda x: x + ['Synergy_Head_Back'])],
  'Card_세구_18': [('character_damage_multiplier', lambda x: x * 1.07)],
  'Card_세구_30': [('character_damage_multiplier', lambda x: x * 1.15)],
  '갈망_1': [('attack_speed', lambda x: x + 0.08), ('movement_speed', lambda x: x + 0.08), ('additional_damage', lambda x: x + 0.08)],
  '갈망_2': [('attack_speed', lambda x: x + 0.10), ('movement_speed', lambda x: x + 0.10), ('additional_damage', lambda x: x + 0.10)],
  '갈망_3': [('attack_speed', lambda x: x + 0.12), ('movement_speed', lambda x: x + 0.12), ('additional_damage', lambda x: x + 0.12)],
  '만찬와인': [('attack_speed', lambda x: x + 0.035), ('movement_speed', lambda x: x + 0.065)],
  '만찬와인_2': [('attack_speed', lambda x: x + 0.065), ('movement_speed', lambda x: x + 0.035)],
  
  '달인': [('crit_rate', lambda x: x + 0.07), ('additional_damage', lambda x: x + 0.085), ('crit_damage', lambda x: x + 0.07)],
  '달인_추피': [('crit_rate', lambda x: x + 0.07), ('additional_damage', lambda x: x + 0.085), ('additional_damage', lambda x: x + 0.031)],
  '회심': [('crit_damage_multiplier', lambda x: x*1.12), ('crit_damage', lambda x: x + 0.07)],
  '회심_추피': [('crit_damage_multiplier', lambda x: x*1.12), ('additional_damage', lambda x: x + 0.031)],
  
  ####### 공통각인 #######
  ## Static ##
  #원한
  'Grudge_1': [('character_damage_multiplier', lambda x: x * 1.04)],
  'Grudge_2': [('character_damage_multiplier', lambda x: x * 1.10)],
  'Grudge_3': [('character_damage_multiplier', lambda x: x * 1.20)],
  #저주받은인형
  'Cursed_Doll_1': [('additional_attack_power', lambda x: x + 0.03)],
  'Cursed_Doll_2': [('additional_attack_power', lambda x: x + 0.08)],
  'Cursed_Doll_3': [('additional_attack_power', lambda x: x + 0.16)],
  #정기흡수
  'Spirit_Absorption_1': [('attack_speed', lambda x: x + 0.03), ('movement_speed', lambda x: x + 0.03)],
  'Spirit_Absorption_2': [('attack_speed', lambda x: x + 0.08), ('movement_speed', lambda x: x + 0.08)],
  'Spirit_Absorption_3': [('attack_speed', lambda x: x + 0.15), ('movement_speed', lambda x: x + 0.15)],
  #예리한둔기
  'Keen_Blunt_Weapon_1': [('crit_damage', lambda x: x + 0.10), ('character_damage_multiplier', lambda x: x * 0.98)],
  'Keen_Blunt_Weapon_2': [('crit_damage', lambda x: x + 0.25), ('character_damage_multiplier', lambda x: x * 0.98)],
  'Keen_Blunt_Weapon_3': [('crit_damage', lambda x: x + 0.50), ('character_damage_multiplier', lambda x: x * 0.98)],
  #아드레날린
  'Adrenaline_1': [('additional_attack_power', lambda x: x + 0.018), ('crit_rate', lambda x: x + 0.05)],
  'Adrenaline_2': [('additional_attack_power', lambda x: x + 0.036), ('crit_rate', lambda x: x + 0.10)],
  'Adrenaline_3': [('additional_attack_power', lambda x: x + 0.06), ('crit_rate', lambda x: x + 0.15)],
  #달인의저력
  'Master\'s_Tenacity_3': [('character_damage_multiplier', lambda x: x * 1.16)],
  #바리케이드 -> TODO: move to buff layer(class specific)
  'Barricade_3': [('character_damage_multiplier', lambda x: x * 1.16)],
  #안정된상태
  'Stabilised_Status_3': [('character_damage_multiplier', lambda x: x * 1.16)],
  #에테르포식자
  'Ether_Predator_1': [('additional_attack_power', lambda x: x + 0.06)],
  'Ether_Predator_3': [('additional_attack_power', lambda x: x + 0.15)],
  #정밀단도
  'Precise_Dagger_3': [('crit_rate', lambda x: x + 0.20), ('crit_damage', lambda x: x - 0.12)],
  #질량증가
  'Increase_Mass_1': [('additional_attack_power', lambda x: x + 0.04), ('attack_speed', lambda x: x - 0.10)],
  'Increase_Mass_2': [('additional_attack_power', lambda x: x + 0.10), ('attack_speed', lambda x: x - 0.10)],
  'Increase_Mass_3': [('additional_attack_power', lambda x: x + 0.18), ('attack_speed', lambda x: x - 0.10)],
  #각성
  'Awakening_1': [('static_buff_queue', lambda x: x + ['Awakening_1'])],
  'Awakening_2': [('static_buff_queue', lambda x: x + ['Awakening_2'])],
  'Awakening_3': [('static_buff_queue', lambda x: x + ['Awakening_3'])],
  ## Dynamic ##
  #돌격대장
  'Raid_Captain_1': [('static_buff_queue', lambda x: x + ['Raid_Captain_1'])],
  'Raid_Captain_2': [('static_buff_queue', lambda x: x + ['Raid_Captain_2'])],
  'Raid_Captain_3': [('static_buff_queue', lambda x: x + ['Raid_Captain_3'])],
  #결투의대가
  'Master_Brawler_1': [('static_buff_queue', lambda x: x + ['Master_Brawler_1'])],
  'Master_Brawler_2': [('static_buff_queue', lambda x: x + ['Master_Brawler_2'])],
  'Master_Brawler_3': [('static_buff_queue', lambda x: x + ['Master_Brawler_3'])],
  #기습의대가
  'Master_Of_Ambush_1': [('static_buff_queue', lambda x: x + ['Master_Of_Ambush_1'])],
  'Master_Of_Ambush_2': [('static_buff_queue', lambda x: x + ['Master_Of_Ambush_2'])],
  'Master_Of_Ambush_3': [('static_buff_queue', lambda x: x + ['Master_Of_Ambush_3'])],
  #타격의대가
  'Hit_Master_1': [('static_buff_queue', lambda x: x + ['Hit_Master_1'])],
  'Hit_Master_2': [('static_buff_queue', lambda x: x + ['Hit_Master_2'])],
  'Hit_Master_3': [('static_buff_queue', lambda x: x + ['Hit_Master_3'])],
  #속전속결
  'All_Out_Attack_1': [('static_buff_queue', lambda x: x + ['All_Out_Attack_1'])],
  'All_Out_Attack_2': [('static_buff_queue', lambda x: x + ['All_Out_Attack_2'])],
  'All_Out_Attack_3': [('static_buff_queue', lambda x: x + ['All_Out_Attack_3'])],
  #슈퍼차지
  'Super_Charge_1': [('static_buff_queue', lambda x: x + ['Super_Charge_1'])],
  'Super_Charge_2': [('static_buff_queue', lambda x: x + ['Super_Charge_2'])],
  'Super_Charge_3': [('static_buff_queue', lambda x: x + ['Super_Charge_3'])],

  ####### 직업각인 #######
  #광기
  # TODO: move to berserker.py
  'Mayhem_1': [('character_damage_multiplier', lambda x: x * 1.03), ('attack_speed', lambda x: x + 0.15), ('movement_speed', lambda x: x + 0.15)],
  'Mayhem_3': [('character_damage_multiplier', lambda x: x * 1.16), ('attack_speed', lambda x: x + 0.15), ('movement_speed', lambda x: x + 0.15)],
  #광전사의비기
  #처단자
  'Punisher_3': [('static_buff_queue', lambda x: x + ['Punisher_Enabled_3'])],
  #포식자
  'Devourer_3': [('static_buff_queue', lambda x: x + ['Devourer_Enabled_3'])],
  #전투태세
  'Combat_Readiness_1': [('static_buff_queue', lambda x: x + ['Combat_Readiness_1'])],
  'Combat_Readiness_3': [('static_buff_queue', lambda x: x + ['Combat_Readiness_3'])],
  #고독한기사
  'Lone_Knight_3': [('static_buff_queue', lambda x: x + ['Lone_Knight_3'])],
  #분노의망치
  'Rage_Hammer_3': [('static_buff_queue', lambda x: x + ['Rage_Hammer_3'])],
  #중력수련
  #오의강화
  #초심
  'First_Intention_1': [('static_buff_queue', lambda x: x + ['First_Intention_1'])],
  'First_Intention_3': [('static_buff_queue', lambda x: x + ['First_Intention_3'])],
  #극의:체술
  'Taijutsu_3': [('static_buff_queue', lambda x: x + ['Taijutsu_3'])],
  #충격단련
  'Shock_Training_3': [('static_buff_queue', lambda x: x + ['Shock_Training_3'])],
  #세맥타통
  'Energy_Overflow_1': [('static_buff_queue', lambda x: x + ['Energy_Overflow_1'])],
  'Energy_Overflow_3': [('static_buff_queue', lambda x: x + ['Energy_Overflow_3'])],
  #역천지체
  'Robust_Spirit_3': [('static_buff_queue', lambda x: x + ['Robust_Spirit_Enabled_3'])],
  #절정
  'Pinnacle_3': [('static_buff_queue', lambda x: x + ['Pinnacle_Enabled_3'])],
  #절제
  'Control_3': [('static_buff_queue', lambda x: x + ['Control_3'])],
  #일격필살
  'Deathblow_3': [('static_buff_queue', lambda x: x + ['Deathblow_3'])],
  #오의난무
  #강화무기 # TODO: move to devilhunter.py
  'Enhanced_Weapon_1': [('crit_rate', lambda x: x + 0.20)],
  'Enhanced_Weapon_3': [('crit_rate', lambda x: x + 0.30)],
  #핸드거너
  'Pistoleer_3': [('static_buff_queue', lambda x: x + ['Pistoleer_3'])],
  #화력강화
  'Firepower_Enhancement_3': [('static_buff_queue', lambda x: x + ['Firepower_Enhancement_3'])],
  #포격강화
  'Barrage_Enhancement_3': [('static_buff_queue', lambda x: x + ['Barrage_Enhancement_3'])],
  #두번째동료
  #죽음의습격
  #아르데타인의기술
  "Arthetinean_Skill_1": [('static_buff_queue', lambda x: x + ['Arthetinean_Skill_1'])],
  "Arthetinean_Skill_3": [('static_buff_queue', lambda x: x + ['Arthetinean_Skill_3'])],
  #진화의유산
  "Evolutionary_Legacy_1": [('static_buff_queue', lambda x: x + ['Evolutionary_Legacy_Enabled_1'])],
  "Evolutionary_Legacy_3": [('static_buff_queue', lambda x: x + ['Evolutionary_Legacy_Enabled_3'])],
  #사냥의시간
  "Time_To_Hunt_1": [('static_buff_queue', lambda x: x + ['Time_To_Hunt_1'])],
  "Time_To_Hunt_3": [('static_buff_queue', lambda x: x + ['Time_To_Hunt_3'])],
  #피스메이커
  "Peace_Maker_1": [('static_buff_queue', lambda x: x + ['Peace_Maker_1'])],
  "Peace_Maker_3": [('static_buff_queue', lambda x: x + ['Peace_Maker_3'])],
  #상급소환사
  'Master_Summoner_3': [('static_buff_queue', lambda x: x + ['Master_Summoner_3'])],
  #넘치는교감
  'Communication_Overflow_3': [('static_buff_queue', lambda x: x + ['Communication_Overflow_3'])],
  #황후의은총
  #황제의칙령
  #점화
  'Igniter_3': [('static_buff_queue', lambda x: x + ['Igniter_Enabled_3'])],
  #환류
  'Reflux_3': [('static_buff_queue', lambda x: x + ['Reflux_3'])],
  #잔재된기운
  'Remaining_Energy_1': [('static_buff_queue', lambda x: x + ['Remaining_Energy_Enabled_1'])],
  'Remaining_Energy_3': [('static_buff_queue', lambda x: x + ['Remaining_Energy_Enabled_3'])],
  #버스트
  'Burst_1': [('static_buff_queue', lambda x: x + ['Burst_Enabled_1'])],
  'Burst_3': [('static_buff_queue', lambda x: x + ['Burst_Enabled_3'])],
  #완벽한억제
  "Perfect_Suppression_1": [('static_buff_queue', lambda x: x + ['Perfect_Suppression_1'])],
  #멈출수없는충동
  "Demonic_Impulse_3": [('static_buff_queue', lambda x: x + ['Demonic_Impulse_3'])],
  #갈증
  "Hunger_3": [('static_buff_queue', lambda x: x + ['Hunger_3'])],
  #달의소리
  "Lunar_Voice_3": [('static_buff_queue', lambda x: x + ['Lunar_Voice_3'])],
  #이슬비
  "Drizzle_3": [('static_buff_queue', lambda x: x + ['Drizzle_Enabled_3'])],
  #질풍노도
  "Gale_Rage_3": [('static_buff_queue', lambda x: x + ['Gale_Rage_3'])],
}

# Data for equipment_layer
# Artifact Sets
ARTIFACT_TABLE = {
  #지배
  '지배_6_1': [('static_buff_queue', lambda x: x + ['Dominion_Set_Enabled_1'])],
  '지배_6_2': [('static_buff_queue', lambda x: x + ['Dominion_Set_Enabled_2'])],
  '지배_6_3': [('static_buff_queue', lambda x: x + ['Dominion_Set_Enabled_3'])],
  #악몽(마중)
  '악몽A_6_1': [('static_buff_queue', lambda x: x + ['Nightmare_Set_Addiction_1'])],
  '악몽A_6_2': [('static_buff_queue', lambda x: x + ['Nightmare_Set_Addiction_2'])],
  '악몽A_6_3': [('static_buff_queue', lambda x: x + ['Nightmare_Set_Addiction_3'])],
  #악몽(끝마)
  '악몽B_6_1': [('static_buff_queue', lambda x: x + ['Nightmare_Set_Boundless_1'])],
  '악몽B_6_2': [('static_buff_queue', lambda x: x + ['Nightmare_Set_Boundless_2'])],
  '악몽B_6_3': [('static_buff_queue', lambda x: x + ['Nightmare_Set_Boundless_3'])],
  #구원
  '구원_6_1': [('additional_damage', lambda x: x + 0.42),
               ('attack_speed', lambda x: x + 0.10),
               ('character_damage_multiplier', lambda x: x * 1.05)],
  '구원_6_2': [('additional_damage', lambda x: x + 0.54),
               ('attack_speed', lambda x: x + 0.10),
               ('character_damage_multiplier', lambda x: x * 1.05)],
  '구원_6_3': [('additional_damage', lambda x: x + 0.63),
               ('attack_speed', lambda x: x + 0.10),
               ('character_damage_multiplier', lambda x: x * 1.06)],
  #사멸
  '사멸_6_1': [('static_buff_queue', lambda x: x + ['Entropy_Set_1'])],
  '사멸_6_2': [('static_buff_queue', lambda x: x + ['Entropy_Set_2'])],
  '사멸_6_3': [('static_buff_queue', lambda x: x + ['Entropy_Set_3'])],
  #환각
  '환각_6_1': [('character_damage_multiplier', lambda x: x * 1.25),
               ('crit_rate', lambda x: x + 0.20)],
  '환각_6_2': [('character_damage_multiplier', lambda x: x * 1.29),
               ('crit_rate', lambda x: x + 0.25)],
  '환각_6_3': [('character_damage_multiplier', lambda x: x * 1.32),
               ('crit_rate', lambda x: x + 0.28)],
  #2악4구
  '2악4구_1': [('attack_speed', lambda x: x + 0.10), ('static_buff_queue', lambda x: x + ['Nig2_Sal4_Set_1'])],
  '2악4구_2': [('attack_speed', lambda x: x + 0.10), ('static_buff_queue', lambda x: x + ['Nig2_Sal4_Set_2'])],
  '2악4구_3': [('attack_speed', lambda x: x + 0.10), ('static_buff_queue', lambda x: x + ['Nig2_Sal4_Set_3'])],
}

# Data for StatFactory
# 일리아칸(Akkan) is base for this table
# 0~25 for ancient, 26,27,28 -> sidereal(에스더) 6, 7, 8
# base level is 1525, 5 for each upgrade
# until upgrade 2(< level 1540), relic accessories take part in stat. after that, ancient accessories take part
STAT_BY_UPGRAGE_TABLE = {
    'armor': [
        107407,
        109803, 112253, 114757, 117317, 119934,
        122608, 125344, 128139, 130997, 133917,
        136904, 139956, 143076, 147882, 152851,
        157985, 163290, 168774, 174442, 180300,
        186355, 192613, 199078, 205762, 212668,
        212668, 212668, 212668,
    ],
    'weapon': [
        37831,
        38673, 39534, 40413, 41313, 42232,
        43172, 44132, 45114, 46118, 47145, 
        48194, 49266, 50362, 52051, 53796,
        55599, 57463, 59390, 61381, 63439,
        65566, 67764, 70036, 72384, 74811,
        75185, 78084, 81095,
    ],
    'accessories' : [
        39488,
        39488, 39488, 50184, 50184, 50184,
        50184, 50184, 50184, 50184, 50184, 
        50184, 50184, 50184, 50184, 50184,
        50184, 50184, 50184, 50184, 50184,
        50184, 50184, 50184, 50184, 50184, 
        50184, 50184, 50184,
    ]
}

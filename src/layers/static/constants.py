"""
Constants for static part of simulator
"""

# Data for character_layer
# Combat Stats Related
CRITICAL_RATE_PER_CRIT = 1 / 27.944 / 100
COOLDOWN_REDUCTION_PER_SWIFTNESS = 1 / 46.5731 / 100
ATTACK_SPEED_PER_SWIFTNESS = 1 / 58.2449 / 100
MOVEMENT_SPEED_PER_SWIFTNESS = 1 / 58.2211 / 100

# Awakening Damage
AWAKENING_DAMAGE_PER_SPECIALIZATION = 1 / 18.3020 / 100


# Data for engraving_layer
# Static Engravings
ENGRAVINGS = {
  ####### Helper각인 #######
  #헬모드
  'Hell': [('additional_damage', lambda x: x - 0.30)],
  'Synergy_Crit_A': [('crit_rate', lambda x: x + 0.10)],
  'Synergy_Crit_B': [('crit_rate', lambda x: x + 0.18)],
  'Synergy_Damage_A': [('damage_multiplier', lambda x: x * 1.06)],
  'Synergy_Damage_B': [('damage_multiplier', lambda x: x * 1.072)],
  'Synergy_Head_Back': [('static_buff_queue', lambda x: x + ['Synergy_Head_Back'])],

  ####### 공통각인 #######
  ## Static ##
  #원한
  'Grudge_3': [('damage_multiplier', lambda x: x * 1.20)],
  #저주받은인형
  'Cursed_Doll_3': [('additional_attack_power', lambda x: x + 0.16)],
  #정기흡수
  'Spirit_Absorption_2': [('attack_speed', lambda x: x + 0.08), ('movement_speed', lambda x: x + 0.08)],
  'Spirit_Absorption_3': [('attack_speed', lambda x: x + 0.15), ('movement_speed', lambda x: x + 0.15)],
  #예리한둔기
  'Keen_Blunt_Weapon_3': [('crit_damage', lambda x: x + 0.50), ('damage_multiplier', lambda x: x * 0.98)],
  #아드레날린
  'Adrenaline_2': [('additional_attack_power', lambda x: x + 0.036), ('crit_rate', lambda x: x + 0.10)],
  'Adrenaline_3': [('additional_attack_power', lambda x: x + 0.06), ('crit_rate', lambda x: x + 0.15)],
  #달인의저력
  'Master’s_Tenacity_3': [('damage_multiplier', lambda x: x * 1.16)],
  #바리케이드 -> TODO: move to buff layer(class specific)
  'Barricade_3': [('damage_multiplier', lambda x: x * 1.16)],
  #안정된상태
  'Stabilised_Status_3': [('damage_multiplier', lambda x: x * 1.16)],
  #에테르포식자
  'Ether_Predator_1': [('additional_attack_power', lambda x: x + 0.06)],
  'Ether_Predator_3': [('additional_attack_power', lambda x: x + 0.15)],
  #정밀단도
  'Precise_Dagger_3': [('crit_rate', lambda x: x + 0.20), ('crit_damage', lambda x: x - 0.12)],
  #질량증가
  'Increase_Mass_3': [('additional_attack_power', lambda x: x + 0.18), ('attack_speed', lambda x: x - 0.10)],
  #각성
  'Awakening_2': [('awakening_cooldown_percentage', lambda x: x + (1-x) * 0.25)],
  'Awakening_3': [('awakening_cooldown_percentage', lambda x: x + (1-x) * 0.50)],
  ## Dynamic ##
  #돌격대장
  'Raid_Captain_3': [('static_buff_queue', lambda x: x + ['Raid_Captain_3'])],
  #결투의대가
  'Master_Brawler_3': [('static_buff_queue', lambda x: x + ['Master_Brawler_3'])],
  #기습의대가
  'Master_Of_Ambush_3': [('static_buff_queue', lambda x: x + ['Master_Of_Ambush_3'])],
  #타격의대가
  'Hit_Master_3': [('static_buff_queue', lambda x: x + ['Hit_Master_3'])],
  #속전속결
  'All_Out_Attack_3': [('static_buff_queue', lambda x: x + ['All_Out_Attack_3'])],
  #슈퍼차지
  'Super_Charge_3': [('static_buff_queue', lambda x: x + ['Super_Charge_3'])],

  ####### 직업각인 #######
  #광기
  'Mayhem_1': [('damage_multiplier', lambda x: x * 1.03), ('attack_speed', lambda x: x + 0.15), ('movement_speed', lambda x: x + 0.15)],
  'Mayhem_3': [('damage_multiplier', lambda x: x * 1.16), ('attack_speed', lambda x: x + 0.15), ('movement_speed', lambda x: x + 0.15)],
  #광전사의비기

  #전투태세 TODO: move to dynamic buff
  'Combat_Readiness_1': [('damage_multiplier', lambda x: x * 1.20),
                         ('awakening_damage_multiplier', lambda x: x / 1.20),
                         ('damage_multiplier', lambda x: x * 1.12)],
  'Combat_Readiness_3': [('damage_multiplier', lambda x: x * 1.20),
                         ('awakening_damage_multiplier', lambda x: x / 1.20),
                         ('damage_multiplier', lambda x: x * 1.18)],
  #고독한기사
  'Lone_Knight_3': [('static_buff_queue', lambda x: x + ['Lone_Knight_3'])],
  #분노의망치
  #중력수련
  #오의강화
  #초심
  'First_Intention_1': [('damage_multiplier', lambda x: x * 1.16)],
  'First_Intention_3': [('damage_multiplier', lambda x: x * 1.32)],
  #극의:체술
  #충격단련
  #세맥타통
  #역천지체
  #절정
  #절제
  'Control_3': [('damage_multiplier', lambda x: x * 1.36), ('awakening_damage_multiplier', lambda x: x / 1.36)],
  #일격필살
  #오의난무
  #강화무기
  'Enhanced_Weapon_1': [('crit_rate', lambda x: x + 0.20)],
  'Enhanced_Weapon_3': [('crit_rate', lambda x: x + 0.30)],
  #핸드거너
  #화력강화
  #포격강화
  #두번째동료
  #죽음의습격
  #아르데타인의기술
  #진화의유산
  #사냥의시간
  'Time_To_Hunt_1': [('crit_rate', lambda x: x + 0.20)],
  'Time_To_Hunt_3': [('crit_rate', lambda x: x + 0.40)],
  #피스메이커
  #상급소환사
  'Master_Summoner_3': [('damage_multiplier', lambda x: x * 1.15)],
  #넘치는교감
  #황후의은총
  #황제의칙령
  #점화

  #환류 TODO: move to dynamic buff
  'Reflux_1': [('damage_multiplier', lambda x: x * 1.08),
               ('awakening_damage_multiplier', lambda x: x / 1.08),
               ('cooldown_percentage', lambda x: x + (1-x) * 0.03),
               ('awakening_cooldown_percentage', lambda x: x - (1-x) * 0.03)],
  'Reflux_3': [('damage_multiplier', lambda x: x * 1.16),
               ('awakening_damage_multiplier', lambda x: x / 1.16),
               ('cooldown_percentage', lambda x: x + (1-x) * 0.10),
               ('awakening_cooldown_percentage', lambda x: x - (1-x) * 0.10)],
  #잔재된기운
  'Remaining_Energy_1': [('damage_multiplier', lambda x: x * 1.12),
                         ('attack_speed', lambda x: x + 0.12),
                         ('movement_speed', lambda x: x + 0.12)],
  'Remaining_Energy_3': [('damage_multiplier', lambda x: x * 1.36),
                         ('attack_speed', lambda x: x + 0.12),
                         ('movement_speed', lambda x: x + 0.12)],
  #버스트
  #멈출수없는충동                         
  #완벽한억제 TODO: move to dynamic buff
  'Perfect_Suppression_1': [('damage_multiplier', lambda x: x * 1.20),
                            ('awakening_damage_multiplier', lambda x: x / 1.20)],
  'Perfect_Suppression_3': [('damage_multiplier', lambda x: x * 1.30),
                            ('awakening_damage_multiplier', lambda x: x / 1.30)],                         
  #갈증
  'Hunger_1': [('damage_multiplier', lambda x: x * 1.12)],
  'Hunger_3': [('damage_multiplier', lambda x: x * 1.25)],
  #달의소리
}

# Data for equipment_layer
# Artifact Sets
ARTIFACT_TABLE = {
  #지배
  '지배_6_1': [('awakening_damage_multiplier', lambda x: x * 0.50),
               ('awakening_cooldown_percentage', lambda x: x + (1-x) * 0.20),
               ('cooldown_percentage', lambda x: x + (1-x) * 0.18),
               ('awakening_cooldown_percentage', lambda x: x - (1-x) * 0.18),
               ('damage_multiplier', lambda x: x * 1.25),
               ('awakening_damage_multiplier', lambda x: x / 1.25),
               ('damage_multiplier', lambda x: x * 1.15)],
  '지배_6_2': [('awakening_damage_multiplier', lambda x: x * 0.70),
               ('awakening_cooldown_percentage', lambda x: x + (1-x) * 0.20),
               ('cooldown_percentage', lambda x: x + (1-x) * 0.18),
               ('awakening_cooldown_percentage', lambda x: x - (1-x) * 0.18),
               ('damage_multiplier', lambda x: x * 1.28),
               ('awakening_damage_multiplier', lambda x: x / 1.28),
               ('damage_multiplier', lambda x: x * 1.18)],
  '지배_6_3': [('awakening_damage_multiplier', lambda x: x * 0.90),
               ('awakening_cooldown_percentage', lambda x: x + (1-x) * 0.20),
               ('cooldown_percentage', lambda x: x + (1-x) * 0.18),
               ('awakening_cooldown_percentage', lambda x: x - (1-x) * 0.18),
               ('damage_multiplier', lambda x: x * 1.31),
               ('awakening_damage_multiplier', lambda x: x / 1.31),
               ('damage_multiplier', lambda x: x * 1.20)],
  #악몽
  '악몽A_6_1': [('damage_multiplier', lambda x: x * 1.12),
               ('awakening_damage_multiplier', lambda x: x / 1.12),
               ('additional_damage', lambda x: x + 0.15),
               ('damage_multiplier', lambda x: x * 1.15)],
  '악몽A_6_2': [('damage_multiplier', lambda x: x * 1.15),
               ('awakening_damage_multiplier', lambda x: x / 1.15),
               ('additional_damage', lambda x: x + 0.18),
               ('damage_multiplier', lambda x: x * 1.18)],
  '악몽A_6_3': [('damage_multiplier', lambda x: x * 1.17),
               ('awakening_damage_multiplier', lambda x: x / 1.17),
               ('additional_damage', lambda x: x + 0.20),
               ('damage_multiplier', lambda x: x * 1.20)],
  #구원
  '구원_6_1': [('additional_damage', lambda x: x + 0.42),
               ('attack_speed', lambda x: x + 0.10),
               ('damage_multiplier', lambda x: x * 1.05)],
  '구원_6_2': [('additional_damage', lambda x: x + 0.54),
               ('attack_speed', lambda x: x + 0.10),
               ('damage_multiplier', lambda x: x * 1.05)],
  '구원_6_3': [('additional_damage', lambda x: x + 0.63),
               ('attack_speed', lambda x: x + 0.10),
               ('damage_multiplier', lambda x: x * 1.06)],
  #사멸
  '사멸_6_1': [('static_buff_queue', lambda x: x + ['Entropy_Set_1'])],
  '사멸_6_2': [('static_buff_queue', lambda x: x + ['Entropy_Set_2'])],
  '사멸_6_3': [('static_buff_queue', lambda x: x + ['Entropy_Set_3'])],
  #환각
  '환각_6_1': [('damage_multiplier', lambda x: x * 1.25),
               ('crit_rate', lambda x: x + 0.20)],
  '환각_6_2': [('damage_multiplier', lambda x: x * 1.29),
               ('crit_rate', lambda x: x + 0.25)],
  '환각_6_3': [('damage_multiplier', lambda x: x * 1.32),
               ('crit_rate', lambda x: x + 0.28)],
}

# Data for StatFactory
# abrelshud, ancient equipment is base for this table
# 0~25 for ancient, 26,27,28 -> sidereal(에스더) 6, 7, 8
# base level is 1390, 10 for each upgrade 1~20, 5 for each upgrade 21~25
# until upgrade 14(< level 1540), relic accessories take part in stat. after that, ancient accessories take part
STAT_BY_UPGRAGE_TABLE = {
    'armor': [
        55530,
        56653, 57797, 60086, 63657, 67436,
        71440, 75683, 80175, 88057, 92032,
        96186, 100527, 105062, 109803, 114757,
        119934, 125344, 130997, 136904, 143076,
        147882, 152851, 157985, 163290, 168774,
        168774, 168774, 168774,
    ],
    'weapon': [
        19607,
        20001, 20403, 21207, 22461, 23790,
        25196, 26686, 28264, 31033, 32430, 
        33889, 35414, 37008, 38673, 40413,
        42232, 44132, 46118, 48194, 50362,
        52051, 53796, 55599, 57463, 59390,
        61800, 63160, 64519,
    ],
    'accessories' : [
        39488,
        39488, 39488, 39488, 39488, 39488,
        39488, 39488, 39488, 39488, 39488, 
        39488, 39488, 39488, 39488, 50184,
        50184, 50184, 50184, 50184, 50184,
        50184, 50184, 50184, 50184, 50184, 
        50184, 50184, 50184,
    ]
}

# Common constants for computing some stats

# Combat Stats Related
CRITICAL_RATE_PER_CRIT = 1 / 27.944 / 100
COOLDOWN_PERCENTAGE_PER_SWIFTNESS = 1 / 46.5731 / 100
ATTACK_SPEED_PER_SWIFTNESS = 1 / 58.2449 / 100
MOVING_SPEED_PER_SWIFTNESS = 1 / 58.2211 / 100

# 각성 Damage
AWAKENING_DAMAGE_PER_SPECIALIZATION = 1 / 18.3020 / 100

# data for StatFactory
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
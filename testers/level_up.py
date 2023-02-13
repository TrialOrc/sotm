from math import e, pow


"""
This module is for testing leveling up via probability.

`x` is the player's current level

`level_prob` is the probability of the player levelling up every action taken at that level.

Use `level_prob + random.rand() >= 1` to determine if the player levels up.

? Possibly store the output of `level_prob + random.rand()` if < 1 and then add that to `(random.rand() / levelling_attempts)` if levelling ends up taking too long.
    if failed_attempts == 0:
        level_check = level_prob + random.rand()
        if level_check >= 1:
            level += 1
            failed_attempts = 0
        else:
            stored_xp = level_check
            failed_attempts += 1
    else:
        level check = stored_xp + (random.rand() / (failed_attemps + 1))
        if level_check >= 1:
            level += 1
            failed_attempts = 0
        else:
            stored_xp = level_check
            failed_attempts += 1
"""

xp_list = []
xp_list_static = [
    1228824,
    1112977,
    1008052,
    913018,
    826944,
    748985,
    678375,
    614422,
    556499,
    504036,
    456519,
    413482,
    374502,
    339197,
    307221,
    278259,
    252027,
    228268,
    206750,
    187260,
    169607,
    153619,
    139138,
    126022,
    114142,
    103383,
    93638,
    84811,
    76817,
    69576,
    63018,
    57078,
    51699,
    46826,
    42413,
    38415,
    34795,
    31516,
    28546,
    25856,
    23419,
    21212,
    19214,
    17403,
    15763,
    14278,
    12933,
    11715,
    10611,
    9612,
    8706,
    7886,
    7144,
    6471,
    5862,
    5310,
    4810,
    4357,
    3947,
    3576,
    3239,
    2934,
    2658,
    2408,
    2182,
    1977,
    1791,
    1622,
    1470,
    1332,
    1207,
    1093,
    990,
    897,
    813,
    737,
    667,
    605,
    548,
    496,
    450,
    408,
    369,
    334,
    303,
    274,
    249,
    225,
    204,
    185,
    167,
    151,
    137,
    124,
    112,
    101,
    91,
    83,
]
max_xp = 1356729


for x in range(len(xp_list_static)):
    level_prob = xp_list_static[x] / max_xp


for x in range(100):
    level_prob = 0.9981 * pow(e, (-0.099 * x))

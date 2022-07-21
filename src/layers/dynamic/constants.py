""" 
Constants for dynamic part
"""

# constants and hyper parameters for dynamic layers
TICKS_PER_SECOND = 100

"""
Unit transformation
"""
def seconds_to_ticks(seconds):
  return seconds * TICKS_PER_SECOND

def ticks_to_seconds(ticks):
  return ticks / TICKS_PER_SECOND

"""
Jewel convert list
"""
DAMAGE_JEWEL_LIST = [
    0,
    0.03,
    0.06,
    0.09,
    0.12,
    0.15,
    0.18,
    0.21,
    0.24,
    0.30,
    0.40
]

COOLDOWN_JEWEL_LIST = [
    0,
    0.02,
    0.04,
    0.06,
    0.08,
    0.10,
    0.12,
    0.14,
    0.16,
    0.18,
    0.20
]
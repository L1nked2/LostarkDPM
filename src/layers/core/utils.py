"""
Unit transformation
"""
TICKS_PER_SECOND = 100

def seconds_to_ticks(seconds):
  return seconds * TICKS_PER_SECOND

def ticks_to_seconds(ticks):
  return ticks / TICKS_PER_SECOND


class ResourcePacker:
  def __init__(self):
    pass
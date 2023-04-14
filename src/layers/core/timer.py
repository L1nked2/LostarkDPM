"""
simple timer class for simulator
"""

DEFAULT_MAX_TICK = 360000

class SimpleTimer:
  DEFAULT_TICK_INTERVAL = 1

  def __init__(self, max_tick:int=DEFAULT_MAX_TICK, tick_types:list[str]=list(), **kwargs):
    # basic timer components
    self._max_tick = max_tick
    self._elapsed_tick = 0
    # tick informations
    self._tick_types = tick_types
    self._tick_counts = dict()
    self._tick_streaks = dict()
    for tick_type in tick_types:
      self._tick_counts[tick_type] = 0
      self._tick_streaks[tick_type] = 0
    self._prev_tick_types = list()
  
  @property
  def is_expired(self):
    return self._elapsed_tick >= self._max_tick
  
  @property
  def elapsed_tick(self):
    return self._elapsed_tick
  
  @property
  def tick_counts(self):
    return self._tick_counts

  @property
  def tick_streaks(self):
    return self._tick_streaks

  # default tick increase
  def _increase_tick(self, tick:int) -> None:
    self._elapsed_tick += tick
  
  def set_tick_types(self, tick_types:list[str]=list()) -> None:
    for given_tick_type in tick_types:
      # check tick types
      assert given_tick_type in self._tick_types, f'Wrong tick type given, got: {given_tick_type}, candidates: {self._tick_types}'
      # tick counts
      self._tick_counts[given_tick_type] += 1
    self._prev_tick_types = tick_types

  # tick increment with tick type, returns streak which are ended
  def increase_tick(self, tick:int=DEFAULT_TICK_INTERVAL) -> dict[str,int]:
    self._increase_tick(tick)
    ended_streaks = dict()
    # tick streak
    for tt in self._tick_types:
      if tt in self._prev_tick_types:
        self._tick_streaks[tt] += tick
      elif self._tick_streaks[tt] > 0:
        ended_streaks[tt] = self._tick_streaks[tt]
        self._tick_streaks[tt] = 0
    return ended_streaks

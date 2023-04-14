"""
Unit transformation
"""
TICKS_PER_SECOND = 100

def seconds_to_ticks(seconds):
  return seconds * TICKS_PER_SECOND

def ticks_to_seconds(ticks):
  return ticks / TICKS_PER_SECOND


class ResourcePacker:
  def __init__(self, resources:list[object]=list(), option='sum'):
    self._resources = resources
    self._option = option
  
  def get_attribute(self, name):
    attributes = list()
    for obj in self._resources:
      attributes.append(getattr(obj, name, 0))
    if self._option == 'sum':
      return sum(attributes)
    elif self._option == 'raw':
      return attributes
    else:
      raise NotImplementedError
  
  def get_multiple_attributes(self, names:list):
    results = list()
    for name in names:
      results.append(self.get_attribute(name))
    return results
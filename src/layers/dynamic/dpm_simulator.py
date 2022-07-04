from src.layers.dynamic.buffs_manager import BuffsLayer

class DpmSimulator(BuffsLayer):
  def __init__(self, config, **kwargs):
    super(DpmSimulator, self).__init__(**kwargs)
    self.config = config
    # timer in seconds
    self.elapsed = 0
    self.tick = 0.1
    
  def invoke_next_skill(self):
    pass

  def print_progress(self):
    pass
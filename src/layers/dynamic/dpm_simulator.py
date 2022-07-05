from copy import deepcopy
import copy
from src.layers.dynamic.buffs_manager import BuffsManager
from src.layers.dynamic.damage_history import DamageHistory
from src.layers.dynamic.constants import TICKS_PER_SECOND


class DpmSimulator:
  def __init__(self, config, base_character, **kwargs):
    self.config = config
    self.base_character = base_character
    self.current_character = copy.deepcopy(base_character)
    # timer
    self.elapsed_tick = 0
    # damage history manager
    self.damage_history = DamageHistory()
    # buff manager
    self.buff_manager = BuffsManager(self.base_character.class_name)
  
  def test(self):
    print(self.buff_manager.class_buff_table)
    
  def invoke_next_skill(self):
    self.elapsed_tick += self.config['tick']

  def print_progress(self):
    print(f"Elapsed time: {self.elapsed_tick/TICKS_PER_SECOND} s")
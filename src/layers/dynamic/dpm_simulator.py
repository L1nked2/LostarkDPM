from copy import deepcopy
import copy
from src.layers.static.character_layer import CharacterLayer
from src.layers.dynamic.buffs_manager import BuffsManager
from src.layers.dynamic.damage_history import DamageHistory
from src.layers.dynamic.constants import TICKS_PER_SECOND


class DpmSimulator:
  def __init__(self, config, base_character: CharacterLayer, **kwargs):
    self.config = config
    self.base_character = base_character
    # timer
    self.elapsed_tick = 0
    # damage history manager
    self.damage_history = DamageHistory()
    # buff manager
    self.buff_manager = BuffsManager(self.base_character.class_name)
    self.buff_manager.import_buffs(self.base_character.static_buff_queue)
    # skill manager

    # reset stat
    self.reset_stat()
    # initialize tick
    self.sync_tick()

  def reset_stat(self):
    self.current_stat = self.base_character.get_stat_detail()
  
  def sync_tick(self):
    self.buff_manager.update_tick(self.elapsed_tick)
  
  def test(self):
    print(self.buff_manager.class_buff_table)
    self.current_stat['actual_attack_power'] += 10000
    print(self.current_stat)
    print(self.base_character.get_stat_detail())
    self.buff_manager.print_buffs()
    
  def invoke_next_skill(self):
    self.sync_tick(self)
    self.elapsed_tick += self.config['tick']

  def print_progress(self):
    print(f"Elapsed time: {self.elapsed_tick/TICKS_PER_SECOND} s")
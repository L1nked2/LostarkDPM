from ..static.character_layer import CharacterLayer
from .buffs_manager import BuffsManager
from .skills_manager import SkillsManager
from .damage_history import DamageHistory
from .constants import *


class DpmSimulator:
  def __init__(self, config, character_dict, **kwargs):
    self.config = config
    self.base_character = CharacterLayer(**character_dict)
    # timer
    self.elapsed_tick = 0
    # damage history manager
    self.damage_history = DamageHistory()
    # buff manager
    self.buff_manager = BuffsManager(self.base_character)
    # skill manager
    self.skills_manager = SkillsManager(self.base_character)
    # initialize tick
    self.sync_tick()

    print('LostArkDpmSimulator is now ready to run')

  def progress(self):
    pass
  
  def sync_tick(self):
    self.buff_manager.update_tick(self.elapsed_tick)
  
  def test(self):
    print(self.buff_manager.class_buff_table)
    print(self.base_character.get_stat_detail())
    self.buff_manager.print_buffs()
    self.skills_manager.print_skills()
    
  def invoke_next_skill(self):
    self.sync_tick(self)
    self.elapsed_tick += self.config['tick']

  def print_progress(self):
    print(f"Elapsed time: {ticks_to_seconds(self.elapsed_tick)} s")
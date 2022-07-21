import importlib
from ..static.character_layer import CharacterLayer
from .buffs_manager import BuffsManager
from .skills_manager import SkillsManager
from .damage_history import DamageHistory
from .constants import *

DEFAULT_TICK_INTERVAL = 1
MAX_TICK = 1000

class DpmSimulator:
  def __init__(self, character_dict, verbose=False, tick_interval=DEFAULT_TICK_INTERVAL, **kwargs):
    self.verbose = verbose
    self.tick_interval = tick_interval
    self.base_character = CharacterLayer(**character_dict)
    import_target = "src.classes." + self.base_character.class_name
    self.class_module = importlib.import_module(import_target)
    # timer
    self.elapsed_tick = 0
    self.blocked_until = 0
    # damage history manager
    self.damage_history = DamageHistory()
    # buff manager
    self.buffs_manager = BuffsManager(self.base_character)
    # skill manager
    self.skills_manager = SkillsManager(self.base_character)
    # initialize tick
    self.sync_tick()

    print('LostArkDpmSimulator is now ready to run')

  def simulation(self):

    self.elapsed_tick += 1
    pass

  def freeze_character(self):
    self.current_character = self.base_character.copy()
  
  def use_skill(self):
    # check if skill_manager is blocked

    # get skill and calculate damage
    target_skill = self.skills_manager.get_next_skill()
    self.buffs_manager.apply_stat_buffs(self.current_character, target_skill)
    dmg_stats = self.current_character.extract_dmg_stats()
    damage = round(target_skill.calc_damage(**dmg_stats))
    if self.verbose:
      print(f'{target_skill} dealt {damage} on {ticks_to_seconds(self.elapsed_tick)}s')
    # start cooldown and handle triggered_actions
    target_skill.start_cooldown(self.current_character.cooldown_reduction)

    # block skill_manger until delay is over

    return
  
  def sync_tick(self):
    self.buffs_manager.update_tick(self.elapsed_tick)
    self.skills_manager.update_tick(self.elapsed_tick)
  
  def test(self):
    print('default test')
    print(self.base_character.get_stat_detail())
    self.buffs_manager.print_buffs()
    self.skills_manager.print_skills()
    print(self.skills_manager.skill_queue)
    print('main loop test')
    self.freeze_character()
    self.use_skill()
    self.elapsed_tick += 100
    self.sync_tick()
    print(self.current_character.get_stat_detail())
    print('second loop test')
    self.freeze_character()
    self.use_skill()
    self.elapsed_tick += 1
    self.sync_tick()
    self.buffs_manager.print_buffs()
    self.freeze_character()
    self.use_skill()
    self.elapsed_tick += 100
    self.sync_tick()
    self.freeze_character()
    self.use_skill()
    self.elapsed_tick += 100
    self.sync_tick()
    


  def print_progress(self):
    print(f"Elapsed time: {ticks_to_seconds(self.elapsed_tick)} s")
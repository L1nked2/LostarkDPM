import importlib
from ..static.character_layer import CharacterLayer
from .buff_manager import BuffManager
from .skill_manager import SkillManager
from .damage_history import DamageHistory
from .constants import *

DEFAULT_TICK_INTERVAL = 1
MAX_TICK = 6000

class DpmSimulator:
  def __init__(self, character_dict, verbose=False, tick_interval=DEFAULT_TICK_INTERVAL, **kwargs):
    self.verbose = verbose
    self.tick_interval = tick_interval
    self.base_character = CharacterLayer(**character_dict)
    import_target = "src.classes." + self.base_character.class_name
    self.class_module = importlib.import_module(import_target)
    # timer
    self._init_timer()
    # damage history manager
    self.damage_history = DamageHistory()
    # buff manager
    self.buffs_manager = BuffManager(self.base_character)
    # skill manager
    self.skills_manager = SkillManager(self.base_character)
    # initialize tick
    self._sync_tick()

    print('LostArkDpmSimulator is now ready to run')

  def run_simulation(self, max_tick=MAX_TICK):
    while self.elapsed_tick < max_tick:
      self._main_loop()

  def print_result(self):
    print(f'total damage: {self.damage_history.total_damage}')
    print(f"Elapsed time: {ticks_to_seconds(self.elapsed_tick)} s")

  def _init_timer(self):
    self.elapsed_tick = 0
    self.blocked_until = 0
    self.idle_tick = 0
    self.delay_tick = 0
    self.idle_streak = 0

  def _main_loop(self):
    # synchronize tick
    self._sync_tick()
    # check if skill_manager is blocked
    flag = self.skills_manager.is_next_cycle_available()
    # main task
    if flag[0] == False:
      self.idle_streak = 0
      self.delay_tick += DEFAULT_TICK_INTERVAL
    elif flag[1] == False:
      self.idle_streak += 1
      self.idle_tick += DEFAULT_TICK_INTERVAL
    else:
      if self.verbose and self.idle_streak > 0:
        print(f'idle streak ended with {ticks_to_seconds(self.idle_streak)}s')
      self.idle_streak = 0
      self.delay_tick += DEFAULT_TICK_INTERVAL
      self._freeze_character()
      self._use_skill()
    self.elapsed_tick += DEFAULT_TICK_INTERVAL

  def _freeze_character(self):
    self.current_character = self.base_character.copy()
  
  def _use_skill(self):
    # get skill and calculate damage
    target_skill = self.skills_manager.get_next_skill()
    self.buffs_manager.apply_stat_buffs(self.current_character, target_skill)
    dmg_stats = self.current_character.extract_dmg_stats()
    damage = round(target_skill.calc_damage(**dmg_stats))
    self.damage_history.register_damage(target_skill.name, damage, self.elapsed_tick)
    if self.verbose:
      print(f'{target_skill} dealt {damage} on {ticks_to_seconds(self.elapsed_tick)}s')
    # start cooldown and handle triggered_actions
    target_skill.start_cooldown(self.current_character.cooldown_reduction)
    self._handle_triggered_actions(target_skill.triggered_actions)
    # block skill_manger until delay is over
    delay = target_skill.calc_delay(self.current_character.actual_attack_speed)
    self.skills_manager.block_until(self.elapsed_tick + delay)
    # reset skill
    target_skill.reset()
    return
  
  def _handle_triggered_actions(self, triggered_actions):
    for action_name in triggered_actions:
      action_func = getattr(self.class_module, action_name)
      action_func(self.buffs_manager, self.skills_manager)
    return
  
  def _sync_tick(self):
    self.buffs_manager.update_tick(self.elapsed_tick)
    self.skills_manager.update_tick(self.elapsed_tick)
  
  def test(self):
    print('test infos')
    print(self.base_character.get_stat_detail())
    self.buffs_manager.print_buffs()


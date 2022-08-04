import importlib
import math
from ..static.character_layer import CharacterLayer
from .buff_manager import BuffManager
from .skill_manager import SkillManager
from .damage_history import DamageHistory
from .constants import *

DEFAULT_TICK_INTERVAL = 1
MAX_TICK = 300000
DPS_CORRECTION_CONSTANT = 0.4

class DpmSimulator:
  def __init__(self, character_dict, verbose=False, tick_interval=DEFAULT_TICK_INTERVAL, **kwargs):
    self.verbose = verbose
    self.tick_interval = tick_interval
    self.base_character = CharacterLayer(**character_dict)
    self.base_module = importlib.import_module("src.classes.base")
    import_target = "src.classes." + self.base_character.class_name
    self.class_module = importlib.import_module(import_target)
    # timer
    self._init_timer()
    # damage history manager
    self.damage_history = DamageHistory()
    # buff manager
    self.buffs_manager = BuffManager(self.base_character, self.verbose)
    # skill manager
    self.skills_manager = SkillManager(self.base_character)
    # initialize tick
    self._sync_tick()
    # delay statistics
    self.delay_statistics = dict()
    self.delay_score = 0.0
    self.used_skill_count = 0
    self.actual_used_skill_count = 0

    print('LostArkDpmSimulator is now ready to run')

  def run_simulation(self, max_tick=MAX_TICK):
    while self.elapsed_tick < max_tick:
      if self.damage_history.is_stablized():
        print("DPS stabilized, terminating simulation")
        break
      self._main_loop()
    self.delay_score = 1/(math.sqrt(self.delay_score) / self.actual_used_skill_count)

  def print_result(self):
    print(f'Total_damage: {self.damage_history.total_damage}')
    print(f'Actual_DPS: {round(self.damage_history.current_dps * DPS_CORRECTION_CONSTANT)}')
    print(f'Idle_Ratio: {round(self.idle_tick / self.elapsed_tick * 100, 2)} %')
    print(f'Nuking_DPS: {round(self.damage_history.max_nuking_dps * DPS_CORRECTION_CONSTANT)}')
    print(f'Delay_score: {round(self.delay_score, 3)}')
    print(f"Elapsed_time: {ticks_to_seconds(self.elapsed_tick)} s")
    print(f'Rune_ratio: {self.skills_manager.rune_ratio}')
  
  def print_damage_details(self):
    print(self.damage_history.get_damage_details())
  
  def print_delay_statistics(self):
    result = dict()
    for skill_name in self.delay_statistics:
      result[skill_name] = round(self.delay_statistics[skill_name]['avg_delay'], 3)
    print(result)
  
  def print_nuking_cycle(self):
    result = dict()
    for damage_info in self.damage_history.nuking_cycle:
      if damage_info['name'] in result:
        result[damage_info['name']] += damage_info['damage_value']
      else:
        result[damage_info['name']] = damage_info['damage_value']
    print(result)

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
      self._use_skill()
    self._calc_damage_from_buffs()
    self.elapsed_tick += DEFAULT_TICK_INTERVAL

  def _freeze_character(self):
    self.current_character = self.base_character.copy()
  
  def _use_skill(self):
    self._freeze_character()
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
    # update average delay
    if delay > 0:
      self._update_delay_statistics(target_skill.name, delay)
    # reset skill
    target_skill.reset()
    self.used_skill_count += 1
    return

  def _calc_damage_from_buffs(self):
    self._freeze_character()
    self.buffs_manager.apply_stat_buffs(self.current_character, self.skills_manager.dummy_skill)
    # get damage buffs and caclulate damage
    self.buffs_manager.apply_damage_buffs(self.current_character, self.damage_history, self.skills_manager.dummy_skill)
    self.skills_manager.dummy_skill.reset()
  
  def _handle_triggered_actions(self, triggered_actions):
    for action_name in triggered_actions:
      action_func = getattr(self.class_module, action_name, None)
      if action_func is None:
        action_func = getattr(self.base_module, action_name, None)
      if action_func is None:
        raise Exception(f'Wrong action {action_name} given')
      action_func(self.buffs_manager, self.skills_manager)
    return
  
  def _sync_tick(self):
    self.buffs_manager.update_tick(self.elapsed_tick)
    self.skills_manager.update_tick(self.elapsed_tick)
  
  def _update_delay_statistics(self, name, delay):
    delay = ticks_to_seconds(delay)
    if name in self.delay_statistics:
      num = self.delay_statistics[name]['num']
      self.delay_statistics[name]['avg_delay'] = (self.delay_statistics[name]['avg_delay'] * num/(num+1)
                                                  + delay * 1/(num+1))
      self.delay_statistics[name]['num'] = num + 1
    else:
      self.delay_statistics[name] = {'num': 1, 'avg_delay': delay}
    self.delay_score += delay ** 2
    self.actual_used_skill_count += 1
  
  def test(self):
    print('test infos')
    print(self.base_character.get_stat_detail())
    self.buffs_manager.print_buffs()


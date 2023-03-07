import importlib
import math
from re import T
from ..static.character_layer import CharacterLayer
from .skill import Skill
from .buff_manager import BuffManager
from .skill_manager import SkillManager
from .damage_history import DamageHistory
from .constants import *

DEFAULT_TICK_INTERVAL = 1
MAX_TICK = 360000
DPS_CORRECTION_CONSTANT = 0.4

class DpmSimulator:
  def __init__(self, character_dict, verbose=0, max_tick=MAX_TICK, tick_interval=DEFAULT_TICK_INTERVAL, **kwargs):
    # verbose 0: default
    # verbose 1: print damage info
    # verbose 2: print damage info, damage stats, skill info, buff info
    self.verbose = verbose
    self.max_tick = max_tick
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
    self.buffs_manager = BuffManager(self.base_character, self.verbose>0)
    # skill manager
    self.skills_manager = SkillManager(self.base_character)
    # initialize tick
    self._sync_tick()
    # delay statistics
    self.delay_statistics = dict()
    self.delay_score = 0.0
    self.used_skill_count = 0
    self.actual_used_skill_count = 0
    self.delay_score_by_percentage = 0.0
    # idle statistics
    self.idle_score = 0.0
    self.idle_streak_num = 0
    # dpct_statistics
    self.dpct_by_percentage_statistics = dict()
    self.dpct_by_percentage = 0.0

    print('LostArkDpmSimulator is now ready to run')

  def run_simulation(self):
    while self.elapsed_tick < self.max_tick:
      if self.damage_history.is_stablized():
        print("DPS stabilized, terminating simulation")
        break
      self._main_loop()
    if self.damage_history.stablization_flag == False:
      print(f'DPS stablization failed, ratio is {self.damage_history.dps_ratio}')
    self._finalize_statistics()

  def get_result(self):
    result = [round(self.damage_history.current_dps * DPS_CORRECTION_CONSTANT),
                  round(self.damage_history.max_nuking_dps_short * DPS_CORRECTION_CONSTANT),
                  round(self.damage_history.max_nuking_dps_long * DPS_CORRECTION_CONSTANT),
                  round(self.damage_history.max_nuking_dps_awakening * DPS_CORRECTION_CONSTANT)]
    return result

  def print_result(self):
    print(f'Actual_DPS: {round(self.damage_history.current_dps * DPS_CORRECTION_CONSTANT)}')
    print(f'Nuking_W/O_Awaking_Short_DPS: {round(self.damage_history.max_nuking_dps_short * DPS_CORRECTION_CONSTANT)}')
    print(f'Nuking_W/O_Awaking_Long_DPS: {round(self.damage_history.max_nuking_dps_long * DPS_CORRECTION_CONSTANT)}')
    print(f'Nuking_DPS: {round(self.damage_history.max_nuking_dps_awakening * DPS_CORRECTION_CONSTANT)}')
    print(f'DPCT_by_Percentage: {round(self.dpct_by_percentage, 3)}')
    print(f'Idle_Ratio: {round(self.idle_tick / self.elapsed_tick * 100, 2)} %')
    print(f'Idle_Score: {round(self.idle_score, 2)}')
    print(f'Delay_Score: {round(self.delay_score, 3)}')
    print(f'Delay_Score_by_Percentage: {round(self.delay_score_by_percentage, 3)}')
    print(f'Total_Damage: {self.damage_history.total_damage}')
    print(f"Elapsed_Time: {ticks_to_seconds(self.elapsed_tick)} s")
    print(f'Rune_Ratio: {self.skills_manager.rune_ratio}')
  
  def print_damage_details(self):
    print(f'Damage_Details: {self.damage_history.get_damage_details()}')
    
  def print_dpct_details(self):
    print(f'DPCT_by_Percentage: {self.dpct_by_percentage_statistics}')

  def print_delay_statistics(self):
    result = dict()
    for skill_name in self.delay_statistics:
      result[skill_name] = round(self.delay_statistics[skill_name]['avg_delay'], 3)
    print(f'Delay_Statistics: {result}')
  
  def print_nuking_cycle(self):
    result = list()

    for damage_info in self.damage_history.nuking_subhistory_short.max_cycle:
      result.append((damage_info['name'], damage_info['damage_value']))
    print(f'Nuking_W/O_Awaking_Cycle_Short: {result}')
    result.clear()

    for damage_info in self.damage_history.nuking_subhistory_long.max_cycle:
      result.append((damage_info['name'], damage_info['damage_value']))
    print(f'Nuking_W/O_Awaking_Cycle_Long: {result}')
    result.clear()

    for damage_info in self.damage_history.nuking_subhistory_awakening.max_cycle:
      result.append((damage_info['name'], damage_info['damage_value']))
    print(f'Nuking_Cycle: {result}')
    result.clear()    

  def _init_timer(self):
    self.elapsed_tick = 0
    self.blocked_until = 0
    self.idle_tick = 0
    self.delay_tick = 0
    self.idle_streak = 0
  
  def _increase_elapsed_tick(self, tick):
    self.elapsed_tick += tick
  
  def _update_delay_and_idle_info(self, is_character_available, is_skill_available):
    # case1: character is using skill
    if is_character_available == False:
      self.idle_streak = 0
      self.delay_tick += DEFAULT_TICK_INTERVAL
    # case2: character is idle but skill is not available
    elif is_skill_available == False:
      self.idle_streak += DEFAULT_TICK_INTERVAL
      self.idle_tick += DEFAULT_TICK_INTERVAL
    # case3: skill is available, end idle streak
    else:
      if self.verbose > 0 and self.idle_streak > 0:
        print(f'idle streak ended with {ticks_to_seconds(self.idle_streak)}s')
      self._update_idle_statistics(self.idle_streak)
      self.idle_streak = 0
      self.delay_tick += DEFAULT_TICK_INTERVAL

  def _main_loop(self):
    # synchronize tick
    self._sync_tick()
    # update character and skill availability from skills_manager
    is_character_available, is_skill_available = self.skills_manager.is_next_cycle_available()
    self._update_delay_and_idle_info(is_character_available, is_skill_available)
    # check character and skill availability and use skill
    if is_character_available and is_skill_available:
      self._use_skill()
    # calc damages from buffs
    self.buffs_manager.calc_damage_from_buffs(self.damage_history, self.skills_manager)
    self._increase_elapsed_tick(DEFAULT_TICK_INTERVAL)

  def _freeze_character(self):
    self.current_character = self.base_character.copy()
  
  def _calc_skill_damage(self, skill: Skill):
    self.buffs_manager.apply_stat_buffs(self.current_character, skill)
    dmg_stats = self.current_character.extract_dmg_stats()
    damage = round(skill.calc_damage(**dmg_stats))
    # print damage, skill, buff details if verbose is set
    if self.verbose > 1:
      print(dmg_stats)
      skill.print_skill_info()
      self.buffs_manager.print_buffs()
    if self.verbose > 0:
      print(f'{skill} dealt {damage} on {ticks_to_seconds(self.elapsed_tick)}s')
    return damage

  def _update_skill_delay(self, skill: Skill):
    delay = skill.calc_delay(self.current_character.actual_attack_speed)
    return delay

  def _use_skill(self):
    self._freeze_character()
    # get skill 
    target_skill = self.skills_manager.get_next_skill()
    # calculate damage and delay
    damage = self._calc_skill_damage(target_skill)
    delay = self._update_skill_delay(target_skill)
    # start cooldown based on new delay
    target_skill.start_cooldown(self.current_character.cooldown_reduction)
    # handle triggered_actions
    self._handle_triggered_actions(target_skill)
    # block skill_manger until delay is over
    self.skills_manager.block_until(self.elapsed_tick + delay)
    # update average delay
    if delay > 0:
      self._update_delay_statistics(target_skill.name, delay)
    # register damage info
    is_awakening = bool(target_skill.identity_type == "Awakening")
    self.damage_history.register_damage(target_skill.name, damage, delay, is_awakening, self.elapsed_tick)
    # reset skill to undo buffs
    target_skill.reset()
    self.used_skill_count += 1
    return

  def _handle_triggered_actions(self, skill: Skill):
    for action_name in skill.triggered_actions:
      action_func = getattr(self.class_module, action_name, None)
      if action_func is None:
        action_func = getattr(self.base_module, action_name, None)
      if action_func is None:
        raise Exception(f'Wrong action {action_name} given')
      action_func(self.buffs_manager, self.skills_manager, skill)
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
  
  def _update_idle_statistics(self, streak_length):
    self.idle_streak_num += 1
    self.idle_score += streak_length ** 2
  
  def _finalize_statistics(self):
    self.delay_score = 1/(math.sqrt(self.delay_score / self.actual_used_skill_count))
    self.idle_score = (math.sqrt(self.idle_score / self.idle_streak_num))
    for name in self.delay_statistics:
      if self.delay_statistics[name]['avg_delay'] > 0:
        self.dpct_by_percentage_statistics[name] = (self.damage_history.damage_details[name] / (self.delay_statistics[name]['avg_delay'] * self.delay_statistics[name]['num'])
                                                    * self.damage_history.damage_details[name] / self.damage_history.total_damage)
        self.dpct_by_percentage += self.dpct_by_percentage_statistics[name]
        self.delay_score_by_percentage += self.delay_statistics[name]['avg_delay'] * self.damage_history.damage_details[name] / self.damage_history.total_damage
    
  def print_test_info(self):
    print('test info')
    print(self.base_character.get_stat_detail())
    self.buffs_manager.print_buffs()


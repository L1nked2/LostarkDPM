import csv
import numpy as np
import pandas as pd
import math
from collections import deque
from .constants import ticks_to_seconds, seconds_to_ticks

STABILIZATION_THRESHOLD = 0.01 / 100 # 0.01% threshold
MINIMUM_RUNNING_SECONDS = 1500
RECENT_SECONDS = 300
NUKING_SECONDS_SHORT = 6
NUKING_SECONDS_LONG = 8
NUKING_WITH_AWAKENING_SECONDS = 10
EDPS_MIN_SECONDS = 6
EDPS_MAX_SECONDS = 16
EDPS_LINSPACE = np.linspace(EDPS_MIN_SECONDS, EDPS_MAX_SECONDS, math.floor((EDPS_MAX_SECONDS-EDPS_MIN_SECONDS)*10+1))

class Subhistory():
    def __init__(self, max_seconds, awakening_in_max_dps_cycle=False):
      self.damages = deque()
      self.total_damage = 0
      self.cur_dps = 0
      self.max_dps = 0
      self.max_cycle = deque()
      self.max_tick = seconds_to_ticks(max_seconds)
      self.awakening_in_max_dps_cycle = awakening_in_max_dps_cycle
      self.is_awakening_included_in_cycle = False
    
    def _refresh_flags(self):
      for damage in self.damages:
        if damage['is_awakening']:
          self.is_awakening_included_in_cycle = True
          return
      self.is_awakening_included_in_cycle = False
      return
    
    def add_damage_event(self, damage_event):
      damage_value = damage_event['damage_value']
      delay = damage_event['delay']
      tick = damage_event['tick']
      self.damages.append(damage_event)
      self.total_damage += damage_value
      while ((tick + delay) - self.damages[0]['tick']) > self.max_tick:
        old_damage_info = self.damages.popleft()
        self.total_damage -= old_damage_info['damage_value']
      self.cur_dps = self.total_damage / ticks_to_seconds(self.max_tick)

      self._refresh_flags()
      # self._update_max_dps_cycle()

      if self.max_dps < self.cur_dps:
        if self.awakening_in_max_dps_cycle == True:
          self.max_dps = self.cur_dps
          self.max_cycle = self.damages.copy()
        elif self.is_awakening_included_in_cycle == False:
          self.max_dps = self.cur_dps
          self.max_cycle = self.damages.copy()
      
    def get_max_info(self):
      return self.max_dps, self.max_cycle

class DamageHistory:
    def __init__(self):
        self.history = list()
        self.total_damage = 0
        self.total_skill_count = 0
        self.last_tick = 0
        self.current_dps = 0.0
        self.dps_ratio = 0.0
        self.stablization_flag = False

        self.damage_details = dict()
        self.skill_counts = dict()

        # add sub_histories for dps statistics
        self.sub_histories = list()
        for i in EDPS_LINSPACE:
          self.sub_histories.append(Subhistory(i))
        self.max_nuking_dps_short = 0
        self.max_nuking_dps_long = 0
        self.max_nuking_dps_awakening = 0

        # recent statistics
        self.recent_subhistory = Subhistory(RECENT_SECONDS)
        self.recent_dps = 0

        # nuking statistics
        self.nuking_subhistory_short = Subhistory(NUKING_SECONDS_SHORT)
        self.nuking_subhistory_long = Subhistory(NUKING_SECONDS_LONG)
        self.nuking_subhistory_awakening = Subhistory(NUKING_WITH_AWAKENING_SECONDS, True)

    def register_damage(self, name, damage_value, delay, is_awakening: bool, tick):
        damage_event = dict(name=name, damage_value=damage_value, delay=delay, is_awakening=is_awakening, tick=tick)
        self.history.append(damage_event)
        self.total_damage += damage_value
        self.last_tick = max(self.last_tick, tick)
        self._update_damage_statistics(damage_event)
        if self.last_tick > 0:
          self.current_dps = self.total_damage / ticks_to_seconds(self.last_tick)

    def is_stablized(self):
        if self.last_tick < seconds_to_ticks(MINIMUM_RUNNING_SECONDS):
          return False
        self.dps_ratio = self.recent_dps / self.current_dps
        if (self.recent_dps < self.current_dps * (1-STABILIZATION_THRESHOLD) 
            or self.recent_dps > self.current_dps * (1+STABILIZATION_THRESHOLD)):
          return False
        else:
          self.stablization_flag = True
          return True
    
    # get subhistory by seconds
    def get_subhistory(self, seconds) -> Subhistory:
        return self.sub_histories[math.floor((seconds-EDPS_MIN_SECONDS)*10)]

    def get_damage_details(self):
        return self.damage_details
    
    def get_edps_statistics(self):
        edps_list = list()
        for second in EDPS_LINSPACE:
          sh = self.get_subhistory(second)
          edps_list.append(sh.max_dps)
        return edps_list

    def get_history(self):
        return self.history
    
    def save_damage_details(self, path):
        f = open(path,'w', newline='')
        wr = csv.writer(f)
        wr.writerow(['name','damage_value'])
        for damage in self.get_damage_details():
            wr.writerow([damage['name'], damage['damage_value']])
    
    def save_edps_statistics(self, path):
        f = open(path,'w', newline='')
        wr = csv.writer(f)
        wr.writerow(list(i for i in EDPS_LINSPACE))
        edps_list = list()
        for second in EDPS_LINSPACE:
          sh = self.get_subhistory(second)
          edps_list.append(sh.max_dps)
        wr.writerow(edps_list)
    
    def _update_damage_statistics(self, damage_event):
        # damage_details
        self._update_damage_details(damage_event)
        # add damage event to all subhistory
        sh: Subhistory
        for sh in self.sub_histories:
          sh.add_damage_event(damage_event)
        # recent_dps
        self.recent_subhistory.add_damage_event(damage_event)
        self.recent_dps = self.recent_subhistory.cur_dps
        # nuking_dps
        self.nuking_subhistory_short.add_damage_event(damage_event)
        self.max_nuking_dps_short = self.nuking_subhistory_short.max_dps
        self.nuking_subhistory_long.add_damage_event(damage_event)
        self.max_nuking_dps_long = self.nuking_subhistory_long.max_dps
        self.nuking_subhistory_awakening.add_damage_event(damage_event)
        self.max_nuking_dps_awakening = self.nuking_subhistory_awakening.max_dps

    def _update_damage_details(self, damage_event):
        name = damage_event['name']
        damage_value = damage_event['damage_value']
        delay = damage_event['delay']
        if name in self.damage_details:
          self.damage_details[name] += damage_value
        else:
          self.damage_details[name] = damage_value
        if name in self.skill_counts:
          self.skill_counts[name] += 1
        else:
          self.skill_counts[name] = 1
        if delay > 0:
          self.total_skill_count += 1
    


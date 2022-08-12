import csv
from collections import deque
from .constants import ticks_to_seconds, seconds_to_ticks


STABILIZATION_THRESHOLD = 0.01 / 100 # 0.01% threshold
MINIMUM_RUNNING_SECONDS = 1500
RECENT_SECONDS = 300
NUKING_SECONDS_SHORT = 6
NUKING_SECONDS_LONG = 8
AWAKENING_NUKING_SECONDS = 10 
MAX_DEALING_TIME_SECONDS = 8
MIN_DEALTIME_SECONDS = 6

class Subhistory():
    def __init__(self, max_time_seconds, awakening_in_max_dps_cycle=False):
      self.damages = deque()
      self.total_damage = 0
      self.cur_dps = 0
      self.max_dps = 0
      self.max_cycle = deque()
      self.max_tick = seconds_to_ticks(max_time_seconds)
      self.awakening_in_max_dps_cycle = awakening_in_max_dps_cycle
      self.is_awakening_included_in_cycle = False
    
    def add_damage_event(self, damage_event):
      damage_value = damage_event['damage_value']
      is_awakening = damage_event['is_awakening']
      tick = damage_event['tick']
      self.damages.append(damage_event)
      self.total_damage += damage_value
      if is_awakening == True:
        self.is_awakening_included_in_cycle = True
      while (tick - self.damages[0]['tick']) > self.max_tick:
        old_damage_info = self.damages.popleft()
        self.total_damage -= old_damage_info['damage_value']
        if old_damage_info['is_awakening'] == True:
          self.is_awakening_included_in_cycle = False
      self.cur_dps = self.total_damage / ticks_to_seconds(self.max_tick)

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
        self.last_tick = 0
        self.current_dps = 0.0
        self.dps_ratio = 0.0
        self.stablization_flag = False

        self.damage_details = dict()

        # recent statistics
        self.recent_subhistory = Subhistory(RECENT_SECONDS)
        self.recent_dps = 0

        # nuking statistics
        self.nuking_subhistory_short = Subhistory(NUKING_SECONDS_SHORT)
        self.max_nuking_dps_short = 0
        self.nuking_subhistory_long = Subhistory(NUKING_SECONDS_LONG)
        self.max_nuking_dps_long = 0
        self.nuking_subhistory_awakening = Subhistory(AWAKENING_NUKING_SECONDS, True)
        self.max_nuking_dps_awakening = 0

        # dealtime statistics
        self.dealing_time_subhistory = Subhistory(MAX_DEALING_TIME_SECONDS)
        self.max_dealing_time_dps = 0
        self.dealing_time_length = 0

    def register_damage(self, name, damage_value, is_awakening, tick):
        damage_event = dict(name=name, damage_value=damage_value, is_awakening=is_awakening,tick=tick)
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
        self.stablization_flag = True
        return True

    def get_damage_details(self):
        return self.damage_details

    def get_history(self):
        return self.history
    
    def save_damage_details(self, path):
        f = open(path,'w', newline='')
        wr = csv.writer(f)
        wr.writerow(['name','damage_value'])
        for damage in self.get_damage_details():
            wr.writerow([damage['name'], damage['damage_value']])
    
    def _update_damage_statistics(self, damage_event):
        # damage_details
        self._update_damage_details(damage_event)
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
        # dealing_time_dps
        self._update_dealing_time_dps(damage_event)

    def _update_damage_details(self, damage_event):
        name = damage_event['name']
        damage_value = damage_event['damage_value']
        if name in self.damage_details:
          self.damage_details[name] += damage_value
        else:
          self.damage_details[name] = damage_value
    
    def _update_dealing_time_dps(self, damage_event):
        self.dealing_time_subhistory.add_damage_event(damage_event)
        tick = damage_event['tick']
        if self.dealing_time_subhistory.is_awakening_included_in_cycle == False:        
          total_damage = self.dealing_time_subhistory.total_damage
          damages = self.dealing_time_subhistory.damages
          for index in range(len(damages)-1):
            tick_diff = tick - damages[index+1]['tick']
            if tick_diff < seconds_to_ticks(MIN_DEALTIME_SECONDS):
              break
            total_damage -= damages[index]['damage_value']
            dealing_time_dps = total_damage/ticks_to_seconds(tick_diff)
            if self.max_dealing_time_dps < dealing_time_dps:
              self.max_dealing_time_dps = dealing_time_dps
              self.dealing_time_length = ticks_to_seconds(tick_diff)
              self.dealing_time_cycle = list(damages)[index+1:]


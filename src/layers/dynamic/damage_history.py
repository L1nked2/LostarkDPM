import csv
from collections import deque
from .constants import ticks_to_seconds, seconds_to_ticks

STABILIZATION_THRESHOLD = 0.01 / 100 # 0.01% threshold
MINIMUM_SECONDS = 1500
RECENT_SECONDS = 300
NUKING_SECONDS = 8


class DamageHistory:
    def __init__(self):
        self.history = list()
        self.history_dps = list()
        self.statistics = dict()
        self.total_damage = 0
        self.last_tick = 0
        self.current_dps = 0.0
        self.prev_dps = 0.0

        self.damage_details = dict()
        self.recent_damages = deque()
        self.total_recent_damage = 0
        self.recent_dps = 0

        self.nuking_damages = deque()
        self.total_nuking_damage = 0
        self.nuking_dps = 0
        self.max_nuking_dps = 0
        self.nuking_cycle = deque()

    def register_damage(self, name, damage_value, tick):
        self.history.append({"name": name, "damage_value": damage_value, "tick": tick})
        self.total_damage += damage_value
        self.last_tick = max(self.last_tick, tick)
        self._update_damage_statistics(name, damage_value, tick)

        self.history_dps.append(self.current_dps)
        self.prev_dps = self.current_dps
        if self.last_tick > 0:
          self.current_dps = self.total_damage / ticks_to_seconds(self.last_tick)

    def is_stablized(self):
        if self.last_tick < seconds_to_ticks(MINIMUM_SECONDS):
          return False
        if (self.recent_dps < self.current_dps * (1-STABILIZATION_THRESHOLD) 
            or self.recent_dps > self.current_dps * (1+STABILIZATION_THRESHOLD)):
            return False
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
    
    def _update_damage_statistics(self, name, damage_value, tick):
        self._update_damage_details(name, damage_value)
        self._update_recent_dps(name, damage_value, tick)
        self._update_nuking_dps(name, damage_value, tick)
    
    def _update_damage_details(self, name, damage_value):
        if name in self.damage_details:
          self.damage_details[name] += damage_value
        else:
          self.damage_details[name] = damage_value

    def _update_recent_dps(self, name, damage_value, tick):
        self.recent_damages.append(dict(name=name, damage_value=damage_value, tick=tick))
        self.total_recent_damage += damage_value
        while (tick - self.recent_damages[0]['tick']) > seconds_to_ticks(RECENT_SECONDS):
          old_damage_info = self.recent_damages.popleft()
          self.total_recent_damage -= old_damage_info['damage_value']
        self.recent_dps = self.total_recent_damage / RECENT_SECONDS
    
    def _update_nuking_dps(self, name, damage_value, tick):
        self.nuking_damages.append(dict(name=name, damage_value=damage_value, tick=tick))
        self.total_nuking_damage += damage_value
        while (tick - self.nuking_damages[0]['tick']) > seconds_to_ticks(NUKING_SECONDS):
          old_damage_info = self.nuking_damages.popleft()
          self.total_nuking_damage -= old_damage_info['damage_value']
        self.nuking_dps = self.total_nuking_damage / NUKING_SECONDS
        if self.max_nuking_dps < self.nuking_dps:
          self.max_nuking_dps = self.nuking_dps
          self.nuking_cycle = self.nuking_damages.copy()
    

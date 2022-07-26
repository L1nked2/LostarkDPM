import csv
from .constants import ticks_to_seconds
# TODO: 8 seconds damage

THRESHOLD = 0.03
EARLY_STOPPING_ROUNDS = 1000

class DamageHistory:
    def __init__(self):
        self.history = list()
        self.history_dps = list()
        self.statistics = dict()
        self.total_damage = 0
        self.last_tick = 0
        self.current_dps = 0.0
        self.prev_dps = 0.0

    def register_damage(self, name, damage_value, tick):
        self.history.append({"name": name, "damage_value": damage_value, "tick": tick})
        self.total_damage += damage_value
        self.last_tick = max(self.last_tick, tick)
        self.history_dps.append(self.current_dps)
        self.prev_dps = self.current_dps
        if self.last_tick > 0:
          self.current_dps = self.total_damage / ticks_to_seconds(self.last_tick)

    def is_stablized(self):
        if len(self.history) < EARLY_STOPPING_ROUNDS:
          return False
        for dps_temp in self.history_dps[:-EARLY_STOPPING_ROUNDS]:
          if (dps_temp < self.current_dps * (1-THRESHOLD) 
              or dps_temp > self.current_dps * (1+THRESHOLD)):
              return False
        return True

    def get_damage_details(self):
        self.damage_details = dict()
        for damage in self.history:
            name = damage['name']
            damage_value = damage['damage_value']
            if name in self.damage_details:
                self.damage_details[name] += damage_value
            else:
                self.damage_details[name] = damage_value

        return self.damage_details

    def get_history(self):
        return self.history
    
    def save_history(self, path):
        f = open(path,'w', newline='')
        wr = csv.writer(f)
        wr.writerow(['tick','name','damage_value'])
        for damage in self.history:
            wr.writerow([damage['tick'], damage['name'], damage['damage_value']])

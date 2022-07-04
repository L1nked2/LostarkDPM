import csv
# TODO: elbow method

class DamageHistory:
    def __init__(self):
        self.history = list()
        self.statistics = dict()
        self.total_damage = 0.0
        self.last_tick = 0
        self.current_dps = 0.0
        self.prev_dps = 0.0

    def register_damage(self, name, damage_value, tick):
        self.history.append({"name": name, "damage_value": damage_value, "tick": tick})
        self.total_damage += damage_value
        self.last_tick = max(self.last_tick, tick)
        self.prev_dps = self.current_dps
        self.current_dps = self.total_damage / self.last_tick

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

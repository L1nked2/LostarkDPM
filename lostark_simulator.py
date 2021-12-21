# lostark simulator

class Simulator:
    def __init__(self):
        self.character = None
        self.damage_dealt = 0


class player_policy:
    def __init__(self):
        self.skill_list = []
        self.skill_priority = None


class Character:
    # debuffs treated as buffs
    def __init__(self):
        self.equipment = None
        self.player_class = None
        self.jewelry = None
        self.buffs = None


class Skill:
    def __init__(self):
        self.level = None
        self.skill_class_type = None  # common, devil(demonic), etc.
        self.skill_common_type = None  # charge, hold, combo, etc.

        self.tripod = None
        self.identity_charge = None  # negative if skill uses


class Damage:
    def __init__(self):
        self.damage_instant = None
        self.element_type_instant = None
        self.damage_sustain = None
        self.element_type_sustain = None

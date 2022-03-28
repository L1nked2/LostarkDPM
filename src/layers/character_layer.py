class CharacterLayer:
    """
    The base layer of simulator (or another name)
    """
    def __init__(self, character_stat):

        # Strength, Dexterity, or Intelligence
        self.stat = 0

        # Combat Stats
        self.crit = 0
        self.specialization = 0
        self.domination = 0
        self.swiftness = 0
        self.endurance = 0
        self.expertise = 0

        # Damage Related
        self.weapon_power = 0
        self.additional_damage = 0
        self.attack_power = 0
        self.attack_speed = 100
        
        # Critical Related
        self.crit_rate = 0.0
        self.crit_damage = 200

    def udpate_attack_power(self, increase=True):
        pass

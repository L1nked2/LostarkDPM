class CharacterLayer:
    """
    The base layer of simlator (or another name)
    """
    def __init__(self):

        # Strength, Dexterity, or Intelligence
        self.stat = 0

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

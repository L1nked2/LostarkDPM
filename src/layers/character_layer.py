from utils import initialize_wrapper

class CharacterLayer:
    """
    Base layer of static part of simulator
    """
    @initialize_wrapper("CharacterLayer", enable_start=False)
    def __init__(self, character_stat):
        self.character_stat = character_stat
       
       # Initialize
        self.initialize_stat()
        self.initialize_combat_stat()
        self.initialize_damage()
        self.initialize_crit()

    def initialize_stat(self):
        self.stat = self.character_stat['stat']
        
    def initialize_combat_stat(self):
        self.combat_stat = self.character_stat['combat_stat']

    def get_combat_stat(self, target):
        return self.combat_stat[target]
        
    def initialize_damage(self):
        # initialize damage based on stats
        self.weapon_power = 0
        self.additional_damage = 0
        self.attack_power = 0
        self.attack_speed = 100
    
    def initialize_crit(self):
        crit = self.get_combat_stat('crit')
        self.crit_rate = 0.000357 * crit
        self.crit_damage = 200
    
    def get_crit_rate(self):
        return self.crit_rate
    
    def get_crit_damage(self):
        return self.crit_damage
    
    def update_crit(self, crit_rate_amount, crit_damage_amount):
        self.crit_rate += crit_rate_amount
        self.crit_damage += crit_damage_amount

    def udpate_attack_power(self, increase=True):
        pass


if __name__ == '__main__':
    
    stat = {
        'stat': 10000,
        'combat_stat': {
            'crit': 1500,
            'specialization': 700,
            'domination': 0,
            'swiftness': 0,
            'endurance': 0,
            'expertise': 0
        }
    }
    # test CharacterLayer class methods
    temp = CharacterLayer(character_stat=stat)
    print(temp.get_combat_stat('crit'))
    print(temp.get_crit_rate(), temp.get_crit_damage())
    temp.update_crit(crit_rate_amount=0.15, crit_damage_amount=50)
    print(temp.get_crit_rate(), temp.get_crit_damage())
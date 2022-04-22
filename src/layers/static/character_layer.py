from db.constants.common import CRITICAL_RATE_PER_CRIT
from src.layers.utils import initialize_wrapper, print_info_wrapper

class CharacterLayer:
    """
    Base layer of static part of simulator
    """
    layer_name = "CharacterLayer"
    
    @initialize_wrapper(layer_name, enable_start=False)
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
        self.weapon_power = self.character_stat['weapon_power']
        self.additional_damage = 0
        self.attack_power = (self.stat * self.weapon_power / 6.0) ** 0.5
        self.additional_attack_power = 0
        self.attack_speed = 100
    
    def initialize_crit(self):
        crit = self.get_combat_stat('crit')
        self.crit_rate = crit * CRITICAL_RATE_PER_CRIT
        self.crit_damage = 200
    
    def get_crit_rate(self):
        return self.crit_rate
    
    def get_crit_damage(self):
        return self.crit_damage
    
    def update_crit(self, crit_rate_amount, crit_damage_amount):
        self.crit_rate += crit_rate_amount
        self.crit_damage += crit_damage_amount

    # Update Method 
    # Usage - update_attribute_with_func('attack_power', lambda x: x * 1.2)
    def update_attribute_with_func(self, attribute_name, update_func):
        try:
            attribute = getattr(self, attribute_name)
        except AttributeError as e:
            print(e)
        else:
            setattr(self, attribute_name, update_func(attribute))
    
    @print_info_wrapper(layer_name)
    def print_character_info(self):
        print("stat:", self.stat)
        print("combat stat:", self.combat_stat)
        print("attack_power:", self.attack_power)

if __name__ == '__main__':
    
    stat = {
        'stat': 10000,
        'weapon_power': 10000,
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
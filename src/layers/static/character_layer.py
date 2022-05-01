from db.constants.common import CRITICAL_RATE_PER_CRIT, COOLDOWN_PERCENTAGE_PER_SWIFTNESS, ATTACK_SPEED_PER_SWIFTNESS, MOVING_SPEED_PER_SWIFTNESS
from src.layers.utils import initialize_wrapper, print_info_wrapper

class CharacterLayer:
    """
    Base layer of static part of simulator
    """
    layer_name = "CharacterLayer"
    
    @initialize_wrapper(layer_name, enable_start=False)
    def __init__(self, character_stat):
        self.character_stat = character_stat
        # Initialize stat
        # include Str, Dex, Int(not distinguished), weapon_power
        # and combat_stat(crit, specialization, swiftness
        # domination, endurance, expertise)
        self.initialize_stat()

        # set initial stat using given stat
        self.reset_stat()

    def initialize_stat(self):
        self.stat = self.character_stat['stat']
        self.weapon_power = self.character_stat['weapon_power']
        combat_stat_attr = ['crit', 'specialization', 'swiftness', 'domination', 'endurance', 'expertise']
        if all (k in self.character_stat['combat_stat'] for k in combat_stat_attr):
            self.combat_stat = self.character_stat['combat_stat']
        else:
            print("character_layer: missing field in combat_stat")
            raise AttributeError        
    
    def reset_stat(self):
        # attack_power
        self.additional_damage = 0
        self.attack_power = (self.stat * self.weapon_power / 6.0) ** 0.5
        self.additional_attack_power = 0
        # crit
        crit = self.combat_stat['crit']
        self.crit_rate = crit * CRITICAL_RATE_PER_CRIT
        self.crit_damage = 2
        # spec -> TODO: init on where?
        specialization = self.combat_stat['specialization']
        # swiftness
        swiftness = self.combat_stat['swiftness']
        self.attack_speed = swiftness * ATTACK_SPEED_PER_SWIFTNESS
        self.moving_speed = swiftness * MOVING_SPEED_PER_SWIFTNESS
        self.cooldown_percentage = swiftness * COOLDOWN_PERCENTAGE_PER_SWIFTNESS
    
    def update_wrapper(func):
        def refresh_function(self, *args, **kwargs):
            res = func(self, *args, **kwargs)
            self.refresh_character_layer()
            return res
        return refresh_function
    
    def get_attribute(self, target):
        try:
            result = getattr(self, target)
        except AttributeError as e:
            print(e)
        else:
            return result

    # Update Method
    @update_wrapper
    def update_attribute(self, target, new_value):
        try:
            getattr(self, target)
        except AttributeError as e:
            print(e)
        else:
            setattr(self, target, new_value)

    # Update Method with first-order function
    # Usage - update_attribute_with_func('attack_power', lambda x: x * 1.2)
    @update_wrapper
    def update_attribute_with_func(self, attribute_name, update_func):
        try:
            attribute = getattr(self, attribute_name)
        except AttributeError as e:
            print(e)
        else:
            setattr(self, attribute_name, update_func(attribute))

    def get_character_detail(self):
        character_detail = dict()
        target_detail = [
            # base attack terms
            'attack_power','additional_damage', 'additional_attack_power',
            # crit terms
            'crit_rate', 'crit_damage',
            # swiftness terms
            'attack_speed', 'moving_speed', 'cooldown_percentage',
        ]
        for item in target_detail:
            character_detail[item] = getattr(self,item)
        return character_detail
    
    def refresh_character_layer(self):
        # self.reset_stat()
        return    
    
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
    print("first details:")
    print(temp.get_character_detail())
    crit_rate_amount = 0.15
    crit_damage_amount = 0.5
    temp.update_attribute_with_func('crit_rate', lambda x: x + crit_rate_amount)
    temp.update_attribute_with_func('crit_damage', lambda x: x + crit_damage_amount)
    print("second details:")
    print(temp.get_character_detail())
from src.layers.static.constants import CRITICAL_RATE_PER_CRIT, COOLDOWN_REDUCTION_PER_SWIFTNESS, ATTACK_SPEED_PER_SWIFTNESS, MOVEMENT_SPEED_PER_SWIFTNESS, AWAKENING_DAMAGE_PER_SPECIALIZATION
from src.layers.static.constants import MAX_MOVEMENT_SPEED, MAX_ATTACK_SPEED
from src.layers.utils import initialize_wrapper, print_info_wrapper, raise_attribute_error
import copy

class StatLayer:
    """
    Base layer of static part of simulator
    """
    layer_name = "StatLayer"

    @initialize_wrapper(layer_name, enable_start=False)
    def __init__(self, character_stat):
        self.character_stat = character_stat
        # Initialize stat
        # include Str, Dex, Int(not distinguished), weapon_power
        # and combat_stat(crit, specialization, swiftness
        # domination, endurance, expertise)
        self.validate_stat()

        # set initial stat using given stat
        self.reset_stat()

    # Import given stat
    def validate_stat(self):
        self.stat = self.character_stat['stat']
        self.weapon_power = self.character_stat['weapon_power']
        combat_stat_attr = ['crit', 'specialization',
                            'swiftness', 'domination', 'endurance', 'expertise']
        if all(k in self.character_stat['combat_stat'] for k in combat_stat_attr):
            self.combat_stat = self.character_stat['combat_stat']
        else:
            raise_attribute_error('StatLayer','missing field in combat_stat')

    # Reset status using given stat and combat_stat
    def reset_stat(self):
        # attack_power
        self.attack_power_base = (
            self.stat * self.weapon_power / 6.0) ** 0.5  # 기본 상태 스탯창 공격력
        # dynamic terms, refresh needed
        # set these terms in bottom layer first, and run refresh_character_layer()
        self.additional_attack_power = 0.0  # 추가 공격력(저받&질증&아드&에포)
        self.additional_damage = 0.30  # 추가피해(equipment(구원,악몽,갈망,파괴), 무품100 -> 0.3 default)
        self.damage_multiplier = 1.00  # 피해증가
        # crit
        crit = self.combat_stat['crit']
        self.crit_rate = crit * CRITICAL_RATE_PER_CRIT
        self.crit_damage = 2.0
        # spec -> TODO: init on where?
        specialization = self.combat_stat['specialization']
        self.specialization = specialization
        #self.awakening_damage_multiplier = specialization * AWAKENING_DAMAGE_PER_SPECIALIZATION
        #self.awakening_cooldown_reduction = 0.0
        # swiftness
        swiftness = self.combat_stat['swiftness']
        self.attack_speed = 1.0 + (swiftness * ATTACK_SPEED_PER_SWIFTNESS)
        self.movement_speed = 1.0 + (swiftness * MOVEMENT_SPEED_PER_SWIFTNESS)
        self.cooldown_reduction = swiftness * COOLDOWN_REDUCTION_PER_SWIFTNESS
        # buff queue
        self.static_buff_queue = list()

        # scale
        self._refresh_stats()
    
    # Refresh stats, called when stats are updated
    def _refresh_stats(self):
        self._calc_useful_stats()

    # Get method
    def get_attribute(self, target):
        try:
            result = getattr(self, target)
        except AttributeError as e:
            print(e)
        else:
            return result

    # Update method
    def update_attribute(self, target, new_value):
        try:
            getattr(self, target)
        except AttributeError as e:
            print(e)
        else:
            setattr(self, target, new_value)
        self._refresh_stats()

    # Update method with first-order function
    # ex) update_attribute_with_func('attack_power', lambda x: x * 1.2)
    def update_attribute_with_func(self, attribute_name, update_func):
        try:
            attribute = getattr(self, attribute_name)
        except AttributeError as e:
            print(e)
        else:
            setattr(self, attribute_name, update_func(attribute))
        self._refresh_stats()

    # Returns character detail in dictionary for further usage
    def get_stat_detail(self):
        character_detail = dict()
        target_detail = [
            # base attack terms
            'attack_power_base', 'additional_attack_power', 'additional_damage', 'damage_multiplier', 'static_buff_queue',
            # useful terms
            'actual_attack_power', 'total_multiplier', 'actual_crit_rate', 'actual_attack_speed', 'actual_movement_speed',
            # crit terms
            'crit_rate', 'crit_damage',
            # spec terms
            'specialization',
            # swiftness terms
            'attack_speed', 'movement_speed', 'cooldown_reduction',
        ]
        for item in target_detail:
            character_detail[item] = getattr(self, item)
        return character_detail

    # Generates hard copy of itself
    def copy(self):
        return copy.deepcopy(self)
    
    # useful stats for actual usage
    # scale some stats
    def _calc_useful_stats(self):
        self.actual_attack_power = self.attack_power_base * (1 + self.additional_attack_power)
        self.total_multiplier = (1 + self.additional_damage) * self.damage_multiplier
        # crit_rate cannot exceed 1
        self.actual_crit_rate = min(self.crit_rate, 1.0)
        # movement_speed and attack_speed cannot exceed 1.4
        self.actual_movement_speed = min(self.movement_speed, MAX_MOVEMENT_SPEED)
        self.actual_attack_speed = min(self.attack_speed, MAX_ATTACK_SPEED)

    @print_info_wrapper(layer_name)
    def print_stat_info(self):
        print(self.get_stat_detail())

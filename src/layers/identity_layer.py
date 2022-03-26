from classes.utils import class_by_name
from combat_stats_layer import CombatStatsLayer

class IdentityLayer(CombatStatsLayer):
    def __init__(self, class_name, stats_spec, jewel_spec, rune_spec):
        super(IdentityLayer, self).__init__(stats_spec, jewel_spec, rune_spec)
        
        self.class_ = class_by_name(class_name)
        pass

    def fetch_identity_info(self):
        pass

    def apply_identity_info(self):
        pass
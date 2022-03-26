from jewel_rune_layer import JewelRuneLayer

class CombatStatsLayer(JewelRuneLayer):
    def __init__(self, stats_spec, jewel_spec, rune_spec):
        super(CombatStatsLayer, self).__init__(jewel_spec, rune_spec)

        self.crit = stats_spec["치명"]
        self.specialization = stats_spec["특화"]
        self.domination = stats_spec["제압"]
        self.swiftness = stats_spec["신속"]
        self.endurance = stats_spec["인내"]
        self.expertise = stats_spec["숙련"]
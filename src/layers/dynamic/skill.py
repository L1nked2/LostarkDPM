class Skill:
    def __init__(self, skill, attack_power, swiftness=0, **kwargs):
        self.name = skill["skill_name"]
        self.damage = []
        self.cooltime = skill["skill_attribute"]["쿨타임"]
        self.tripod_effects = []
        self.additional_attack_speed = 1

        self.compute_damage(skill, attack_power)
        self.save_tripods_to_effects(skill)
        self.compute_possible_static_info(skill, swiftness)

    def compute_damage(self, skill, attack_power):
        skill_default_damage = skill["skill_default_damage"]
        skill_default_coeff = skill["skill_default_coeff"]

        for idx, default in enumerate(skill_default_damage):
            result = default + attack_power * skill_default_coeff[idx]
            self.damage.append(result)
    
    def save_tripods_to_effects(self, skill):
        for i in [1, 2, 3]:
            tokenized_effects = [tuple(effect.split(" ")) for effect in skill[f"skill_tripod_{i}"]]
            self.tripod_effects.extend(tokenized_effects)

    def compute_possible_static_info(self, skill, swiftness):
        # Cooltime
        # e.g. ("cooltime", "+5"), ("cooltime", "-5")
        cooltime_effects = [effect for effect in self.tripod_effects if effect[0] == "cooltime"]

        for effect in cooltime_effects:
            self.cooltime += int(effect[1])
            if self.cooltime < 0:
                warnings.warn(f"Too much reducing cooltime, check skill configuration of {self.name}", UserWarning)
        
        self.cooltime *= (1 - swiftness * COOLDOWN_PERCENTAGE_PER_SWIFTNESS)

        # Frostfire jewel
        frostfire_level = skill["skill_jewel"]["frostfire"]
        for idx, damage in enumerate(self.damage):
            frostfired_damage = damage * (1 + FROSTFIRE_JEWEL_LEVEL_DICT[frostfire_level])
            self.damage[idx] = frostfired_damage

        # Nemesis jewel - to be considered here?

        # Additional attack speed
        ## Rune
        rune_category = skill["skill_rune"]["category"]
        rune_level = skill["skill_rune"]["level"]
        if rune_category == "질풍":
            self.additional_attack_speed *= (1 + get_rune_effect(category=rune_category, level=rune_level))

        ## Tripod
        attack_speed_effects = [effect for effect in self.tripod_effects if effect[1] == "공격속도"]
        for effect in attack_speed_effects:
            self.additional_attack_speed *= (1 + int(effect[2]) / 100)
    
    def print_skill_info(self):
        print(f"Name: {self.name}")
        print(f"Damage: {self.damage}")
        print(f"Cooltime: {self.cooltime}")
from policy_layer import PolicyLayer

class BuffsLayer(PolicyLayer):
    def __init__(self, **kwargs):
        super(BuffsLayer, self).__init__(**kwargs)
    
    def extract_buffs(self):
        skill_tree = self.character_info.skill_tree
        # Do something #
        pass
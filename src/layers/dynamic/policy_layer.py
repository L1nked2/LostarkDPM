from src.layers.dynamic.identity_layer import IdentityLayer

class PolicyLayer(IdentityLayer):
    def __init__(self, policy, **kwargs):
        super(PolicyLayer, self).__init__(**kwargs)
        self.policy = policy
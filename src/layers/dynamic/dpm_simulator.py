from buffs_layer import BuffsLayer

class DpmSimulator(BuffsLayer):
    def __init__(self, config, **kwargs):
        super(DpmSimulator, self).__init__(**kwargs)
        self.config = config
    
    def simulator_method_1(self):
        pass

    def simulator_method_2(self):
        pass
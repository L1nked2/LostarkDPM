from jewel_rune_layer import JewelRuneLayer

class InfoLayer(JewelRuneLayer):
    def __init__(self, config, **kwargs):
        super(InfoLayer, self).__init__(**kwargs)
        self.config = config
    
    def apply_config(self):
        pass
from src.layers.static.jewel_rune_layer import JewelRuneLayer
from src.layers.utils import initialize_wrapper

class InfoLayer(JewelRuneLayer):
    @initialize_wrapper("InfoLayer", enable_start=False)
    def __init__(self, config, **kwargs):
        super(InfoLayer, self).__init__(**kwargs)
        self.config = config
    
    def apply_config(self):
        pass
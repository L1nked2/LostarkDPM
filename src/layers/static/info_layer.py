from src.layers.static.jewel_rune_layer import JewelRuneLayer
from src.layers.utils import initialize_wrapper

class InfoLayer(JewelRuneLayer):
    
    @initialize_wrapper("InfoLayer", enable_start=False)
    def __init__(self, **kwargs):
        super(InfoLayer, self).__init__(**kwargs)
        
    def check_static_layer_initialization(self):
        pass

    def print_layer_info(self, detail=True, layers=["character", "engraving", "equipment", "skiltree"]):
        for layer in layers:
            print_info = getattr(self, "print" + layer + "info")
            print_info(detail=detail)

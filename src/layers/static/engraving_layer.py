from src.layers.static.stat_layer import StatLayer
from src.layers.static.constants import ENGRAVINGS
from src.layers.utils import initialize_wrapper, print_info_wrapper, raise_attribute_error

class EngravingLayer(StatLayer):
  layer_name = "EngravingLayer"

  @initialize_wrapper("EngravingLayer", enable_start=False)
  def __init__(self, engravings, **kwargs):
    super(EngravingLayer, self).__init__(**kwargs)
    self.engravings = engravings
    self.apply_static_engravings()
  
  def apply_static_engravings(self):
    for engraving in self.engravings:
      if engraving in ENGRAVINGS:
        self.apply_one_engraving(engraving)
      else:
        raise_attribute_error('EngravingLayer', 'wrong engraving given, ' + engraving)

  def apply_one_engraving(self, engraving):
    for target, effect in ENGRAVINGS[engraving]:
      super(EngravingLayer, self).update_attribute_with_func(target, effect)
  
  @print_info_wrapper(layer_name)
  def print_engraving_info(self):
    print("engravings:", self.engravings)

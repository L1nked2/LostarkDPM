from src.layers.static.character_layer import CharacterLayer
from db.constants.common import STATIC_ENGRAVINGS
from src.layers.utils import initialize_wrapper, print_info_wrapper



class EngravingLayer(CharacterLayer):
  layer_name = "EngravingLayer"

  @initialize_wrapper("EngravingLayer", enable_start=False)
  def __init__(self, engravings, **kwargs):
    super(EngravingLayer, self).__init__(**kwargs)
    self.engravings = engravings
    self.dynamic_engraving_list = list()
    self.apply_static_engravings()
  
  def apply_static_engravings(self):
    for engraving in self.engravings:
      if engraving in STATIC_ENGRAVINGS:
        self.apply_one_engraving(engraving)
      else:
        self.dynamic_engraving_list.append(engraving)

  def apply_one_engraving(self, engraving):
    for target, effect in STATIC_ENGRAVINGS[engraving]:
      
      super(EngravingLayer, self).update_attribute_with_func(target, effect)
  
  @print_info_wrapper(layer_name)
  def print_engraving_info(self):
    print("engravings:", self.engravings)

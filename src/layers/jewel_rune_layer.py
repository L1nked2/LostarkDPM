from equipment_layer import EquipmentLayer

class JewelRuneLayer(EquipmentLayer):
    def __init__(self, jewel_spec, rune_spec):
        super(JewelRuneLayer, self).__init__()
        self.jewel_spec = jewel_spec
        self.rune_spec = rune_spec

    # validate specs
    def validate(self):
        pass
    # Overriding? or new method?
    def update(self):
        pass
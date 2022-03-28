from skill_tree_layer import SkilTreeLayer

class JewelRuneLayer(SkilTreeLayer):
    def __init__(self, jewel_spec, rune_spec, **kwargs):
        super(JewelRuneLayer, self).__init__(**kwargs)
        self.jewel_spec = jewel_spec
        self.rune_spec = rune_spec

    # validate specs
    def validate(self):
        pass
    # Overriding? or new method?
    def update(self):
        pass
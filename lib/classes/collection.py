from lib.classes.basecardset import BaseCardSet

class Collection(BaseCardSet):
    """Very similar to pack, just linked to a user instead"""

    def __init__(self, *, name=None, owner=None, card_object_list=None):
        if card_object_list is None:
            super().__init__(name=name)
        else:
            super().__init__(name=name, card_object_list=card_object_list)
        self.owner = owner

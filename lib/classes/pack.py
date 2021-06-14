from lib.classes.card import Card

class Pack(list):

    def __init__(self, *, name=None, pack_list=None):
        if pack_list is None:
            super().__init__()
        else:
            card_object_list = [Card(
                id=index+1,
                card_dict=card_dict,
                pack=name
            ) for index, card_dict in enumerate(pack_list)]
            super().__init__(card_object_list)
        self.name = name


    def get_list(self):
        return [card.get_dict() for card in self]

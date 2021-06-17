from lib.classes.card import Card

class BaseCardSet(list):
    """Not a set"""

    def __init__(self, *, name=None, card_dict_list=None, card_object_list=None):
        if card_dict_list is not None:
            object_list = [ Card(
                id=index,
                card_dict=card_dict,
                pack=name
            ) for index, card_dict in enumerate(card_dict_list) ]
        elif card_object_list is not None:
            object_list = card_object_list
        else:
            object_list = []
        super().__init__(object_list)
        self.name = name


    def get_list(self):
        return [ card.get_dict() for card in self ]

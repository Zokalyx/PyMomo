from lib.classes.card import Card


class BaseCardSet(list):
    """Not a set :p"""

    def __init__(
        self,
        *,
        name: str = None,  # Always (pack_name)
        card_dict_list=None,
        card_object_list=None
    ):
        """Creates either a Pack or a Collection given a list of card dicts
        or a list of card objects"""
        self.name = name
        # Loading primitive, dict data
        if card_dict_list is not None:
            # List comprehension
            object_list = [ Card(
                id=index,
                card_dict=card_dict,
                pack_name=name
            ) for index, card_dict in enumerate(card_dict_list) ]
        # Cards already objects
        elif card_object_list is not None:
            object_list = card_object_list
        # Empty set
        else:
            object_list = []
        # Create a list based on the created list of Card instances
        super().__init__(object_list)

    def get_list(self) -> list[dict]:
        """Returns the collection as a list of card dicts for saving"""
        return [card.get_dict() for card in self]

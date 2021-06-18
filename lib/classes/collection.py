from lib.classes.basecardset import BaseCardSet
from lib.classes.card import Card


class Collection(BaseCardSet):
    """Very similar to pack, just linked to a user instead"""

    def __init__(
        self,
        *,
        name: str = None,  # Always (pack_name)
        owner: str = None,  # Always
        card_object_list: list[Card] = None  # Only when loading from existing
    ):
        self.owner = owner
        # Creating a new, empty collection
        if card_object_list is None:
            super().__init__(name=name)
        # Loading collection from data
        else:
            super().__init__(name=name, card_object_list=card_object_list)

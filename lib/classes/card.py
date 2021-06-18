class Card():
    """Card class for Momo trading cards - most elementary abstraction"""

    def __init__(
        self,
        *,
        id: int = None,  # Always
        pack_name: str = None,  # Always
        link: str = None,  # Only when registering new Card
        card_dict: dict = None  # Only when loading Card from data
    ):
        """Creates a card, either from data or by registering a new one"""
        self.id = id
        self.pack = pack_name
        # Creating a brand new card
        if card_dict is None:
            self.link = link
        # Creating instance from data
        else:
            for attr in card_dict:
                setattr(self, attr, card_dict[attr])

    def get_dict(self) -> dict:
        """Returns a dictionary that represents the user and can be saved
        as json. Does not include redundant data, such as id and pack name"""
        excluded = ("id", "pack")
        # Dict comprehension
        return {
            key: value
            for key, value in vars(self).items()
            if key not in excluded
        }

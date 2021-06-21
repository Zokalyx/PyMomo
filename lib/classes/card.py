import time

class Card():
    """Card class for Momo trading cards - most elementary abstraction"""

    def __init__(
        self,
        *,
        id: int = None,  # Always
        pack_name: str = None,  # Always
        rarity: str = None,  # Optional, when registering new Card
        link: str = None,  # Only when registering new Card
        card_dict: dict = None  # Only when loading Card from data
    ):
        """Creates a card, either from data or by registering a new one"""
        self.id = id
        self.pack = pack_name
        self.mult = 1
        self.value = 0
        self.owner = 0
        self.custom = ""
        self.desc = ""
        self.stats = {
            "rolls": 0,
            "reacts": 0,
            "invs": 0,
            "last_roll": {
                "time": 0,
                "user": 0,
            },
            "obtained": {
                "time": 0,
                "user": 0,
                "reason": ""
            },
            "value": [(time.time(), 0)]
        }
        if rarity is None:
            self.rarity = "c"
        else:
            self.rarity = rarity
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

    def get_short(self) -> str:
        """Returns pack and id as a string"""
        return f"{self.pack} {self.id + 1}"

    def get_full(self) -> str:
        """Returns pack, id and custom name as a string"""
        return (
            self.get_short()
            + (f": {self.custom}" if self.custom else "")
        )

    def get_best_name(self) -> str:
        """Returns custom name or short name if there is not any"""
        return self.custom if self.custom else self.get_short()

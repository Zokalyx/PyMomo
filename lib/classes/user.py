import time
import functools
import discord
from lib.classes.card import Card
from lib.classes.collection import Collection
from lib.classes.pack import Pack

class User:
    """Custom User class for Momo players"""

    def __init__(
        self,
        *,
        id: int = None,  # Only when a User is loaded from data
        user_dict: dict = None,  # Only when a User is loaded from data
        user: discord.User = None,  # Only when a new User is registered
        packs: Pack = None  # Always
    ):
        """Creates either a new User using Discord API to retrieve basic data
        or creates a User object from the saved user_dict"""
        self.collection: dict[str, Collection] = {}
        # New user from Discord
        if user_dict is None:
            # Retrieve data
            self.default_name: str = user.display_name
            self.nicks: list[str] = [user.name]
            self.img: str = str(user.avatar_url)
            self.color: int = user.color.value
            self.id: int = user.id
            self.skills = {
                "fire": 0,
                "water": 0,
                "air": 0,
                "earth": 0
            }
            self.lvl = 1
            self.xp = 0
            self.bal = 500
            self.stats = {
                "bal": [(time.time(), self.bal)],
                "rolls": 0,
                "reacts": 0,
                "invs": 0,
                "buys": 0,
                "commands": 0,
                "xp": 0
            }
            self.desc = ""
            # Create a new, empty collection for each existing pack
            for pack_name in packs:
                self.collection[pack_name] = Collection(
                    name=pack_name, owner=self.id
                )
        # Already existing user
        else:
            # Retrieve data
            for attr in user_dict:
                setattr(self, attr, user_dict[attr])
            self.id: int = id
            # Create a collection with owned cards for each existing pack
            for pack_name, pack in packs.items():
                self.collection[pack_name] = Collection(
                    name=pack_name,
                    owner=self.id,
                    card_object_list=self.get_owned_cards_in(pack)
                )

    def get_dict(self) -> dict:
        """Returns a dictionary that represents the user and can be saved
        as json. Does not include redundant data, such as id and collection"""
        excluded = ("id", "collection")
        # Dict comprehension
        return { 
            key: value
            for key, value in vars(self).items()
            if key not in excluded
        }

    def get_owned_cards_in(self, pack: Pack) -> list[Card]:
        """Returns the cards that the user owns in a given pack
        to be used in __init__"""
        # List comprehension
        return [ card for card in pack if card.owner == self.id ]

    def get_rarity_counts(self, proportion=False) -> dict:
        """Returns a dict containing the amount of cards owned for each
        rarity. Optionally returns the proportion of these cards compared
        to the total owned"""
        amounts = {"c": 0, "r": 0, "e": 0, "l": 0, "m": 0}
        count = 0
        for col_name in self.collection:
            for card in self.collection[col_name]:
                amounts[card.rarity] += 1
                count += 1
        # Optionally scale
        if proportion and count != 0:
            for rar in amounts:
                amounts[rar] /= count
        return amounts

    def get_all_cards(self) -> list[Card]:
        """Returns all cards sorted by pack name"""
        return functools.reduce(
            lambda x, y: x+y,
            dict(sorted(self.collection.items())).values(),
            []
        )

    def get_top(self, count=None) -> list[Card]:
        """Returns all cards sorted by total value
        Optionally choose how many cards to return"""
        cards = list(reversed(sorted(self.get_all_cards(), key=lambda x: x.value * x.mult)))
        if count is None:
            return cards
        
        if count > len(cards):
            count = len(cards)
        
        return cards[:count]

    def get_total_value(self, pack_name=None) -> list[Card]:
        """Returns the total value of a card in a given pack
        if None is given, it returns the average value of all cards"""
        if pack_name is None:
            cards = self.get_all_cards()
        else:
            cards = self.collection[pack_name]
        return sum(card.value * card.mult for card in cards)
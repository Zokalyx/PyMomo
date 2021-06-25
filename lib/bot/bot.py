# Fix for Momo.close raising exceptions - Issue with Win 10
# https://github.com/Rapptz/discord.py/issues/5209
import platform
import asyncio
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ----------------------------------------------------------------------------
import functools
from datetime import datetime

import discord
from discord.ext import commands
from lib.classes import User, Pack, Card
from lib.db import Database


class Momo(commands.Bot):
    """Momo bot class containing vital methods and data"""

    def __init__(self, *args, database: Database, **kwargs):
        """Load data from database and start up Bot"""
        self.db: Database = database
        self.unpack_data()
        self.last_modified: datetime = datetime.utcnow()
        self.there_was_change: bool = False
        super().__init__(*args, **kwargs)

    @property
    def users(self) -> dict[int, User]:
        """Fix for Bot already having the users property"""
        return self._users

    def update_last_modified(self) -> None:
        """Used for website caching"""
        self.last_modified = datetime.utcnow()

    def get_user_objects(self) -> dict[int, User]:
        """Returns processed, internal User objects from json (dict) data"""
        user_dict_dict = self.db.data["users"]
        # Dict comprehension
        return {
            int(user_id): User(
                user_dict=user_dict,
                id=int(user_id),
                packs=self.packs
            )
            for user_id, user_dict in user_dict_dict.items()
        }

    def get_user_dicts(self) -> dict[str, dict]:
        """Returns a dict of dicts corresponding to the users for saving"""
        user_object_dict = self.users
        # Dict comprehension
        return {
            str(user_id): user_object.get_dict()
            for user_id, user_object in user_object_dict.items()
        }

    def get_pack_objects(self) -> dict[str, Pack]:
        """Generates processed, internal Pack objects from json(dict) data"""
        pack_list_dict = self.db.data["packs"]
        # Dict comprehension
        return {
            pack_name: Pack(
                name=pack_name,
                card_dict_list=pack_list
            )
            for pack_name, pack_list in pack_list_dict.items()
        }

    def get_pack_lists(self) -> dict[str, list]:
        """Returns a dict of lists corresponding to the packs for saving"""
        pack_object_dict = self.packs
        # Dict comprehension
        return {
            pack_name: pack_object.get_list()
            for pack_name, pack_object in pack_object_dict.items()
        }

    def get_all_cards(self) -> list[Card]:
        """Returns all cards sorted by pack name"""
        return functools.reduce(
            lambda x, y: x+y,
            dict(sorted(self.packs.items())).values(),
            []
        )

    def get_full_collections(self) -> dict[int, list[Card]]:
        """Returns lists of all cards owned by each user as a dict"""
        # Dict comprehension
        return {
            user_id: functools.reduce(
                lambda x, y: x + y,
                user.collection.values(),
                []
            ) for user_id, user in self.users.items()
        }

    def get_sorted_users(self) -> list[tuple[int, User]]:
        """Returns all users sorted by the amount of owned cards"""
        cols = self.get_full_collections()
        return sorted(
            self.users.items(),
            key=lambda x: len(cols[x[0]]),
            reverse=True
        )

    def get_odds(self) -> dict[str, float]:
        """Returns odds for rolling each rarity"""
        weighted_total = 0
        weighted_counts = {
            "c": 0,
            "r": 0,
            "e": 0,
            "l": 0,
            "m": 0
        }
        for pack_name, pack_list in self.packs.items():
            for card in pack_list:
                to_sum = self.config["weights"][card.rarity]
                weighted_total += to_sum
                weighted_counts[card.rarity] += to_sum
        
        if weighted_total != 0:
            for weighted in weighted_counts:
                weighted_counts[weighted] /= weighted_total
            
        return weighted_counts

    def pack_data(self) -> None:
        """Updates the data on the database for it to save it to disk"""
        self.db.data["config"] = self.config
        self.db.data["users"] = self.get_user_dicts()
        self.db.data["packs"] = self.get_pack_lists()

    def unpack_data(self) -> None:
        """Gets the data from the Database instance, creates the objects
        corresponding to them and loads them to this Momo instance"""
        self.config = self.db.data["config"]
        self.packs = self.get_pack_objects()
        self._users = self.get_user_objects()

    def add_cogs(self, cogs: list[commands.Cog]) -> None:
        """Adds all of the passed cogs to this instance of Momo"""
        for cog in cogs:
            self.add_cog(cog(self))

    def run(self, *args, **kwargs) -> None:
        """Runs the bot - is only modified for the connecting message :p"""
        print("Connecting to Discord... ", end="")
        super().run(*args, **kwargs)

#-------------------------------EVENTS----------------------------------------

    async def on_ready(self) -> None:
        """Event listener for when the bot is connected and ready"""
        # Send a message to default channel
        await self.get_channel(
            self.db.data["config"]["default-channel"]
        ).send("✅ En línea")

    async def on_message(self, message: discord.Message) -> None:
        """Event listener for when a message is sent. Ignore all bots,
        create a new User object if the author of the message is not
        registered and process the command if there is any"""
        author = message.author
        # Exclude bots
        if not author.bot:
            # Check if user is already registered
            if author.id not in self.users:
                # Create a new User instance
                self.users[author.id] = User(user=author)
            # Process commands
            await self.process_commands(message)

    async def on_command_error(self, ctx, exception) -> None:
        """Event listener for when a command fails. Overrides default
        behavior for a more expressive one (displays what went wrong)"""
        cmd = ctx.command
        # Command not recognized
        if cmd is None:
            await ctx.send("❌ Comando no reconocido")
        # Command recognized, but something went wrong
        else:
            await ctx.send(
                f"Uso correcto: `{cmd.name} {cmd.usage}`\n{exception}"
            )

    """
    def updates(self, func):
        async def inner(*args, **kwargs):
            self.update_last_modified()
            self.there_was_change = True
            if asyncio.iscoroutinefunction(func):
                await func(*args, **kwargs)
            else:
                func(*args, **kwargs)
        return inner
    """

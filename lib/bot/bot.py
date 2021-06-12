# Fix for Momo.close raising exceptions - Issue with Win 10
# https://github.com/Rapptz/discord.py/issues/5209
import platform
import asyncio
if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ----------------------------------------------------------------------------

from discord.ext import commands
from lib.classes import User

class Momo(commands.Bot):
    
    def __init__(self, *args, database, **kwargs):
        self.db = database
        self.config = 123
        self.config = self.db.data["config"]
        self.cards = self.db.data["cards"]
        self._users = self.get_user_objects()
        super().__init__(*args, **kwargs)


    @property
    def users(self):
        return self._users

    
    def get_user_objects(self):
        user_dicts = self.db.data["users"]
        return { int(d_id): User(user_dict=user_dicts[d_id]) for d_id in user_dicts }


    def get_user_dicts(self):
        user_objects = self.users
        return { str(d_id): user_objects[d_id].get_dict() for d_id in user_objects }


    def pack_data(self):
        self.db.data["config"] = self.config 
        self.db.data["users"] = self.get_user_dicts()
        self.db.data["cards"] = self.cards 


    def add_cogs(self, cogs):
        for cog in cogs:
            self.add_cog(cog(self))


    def run(self, *args, **kwargs):
        print("Connecting to Discord... ", end="")
        super().run(*args, **kwargs)


    async def on_ready(self):
        await self.get_channel(self.db.data["config"]["default-channel"])\
            .send("Online")
        print("Done!")


    async def on_message(self, message):
        author = message.author
        if not author.bot:
            if author.id not in self.users:
                self.users[author.id] = User(user=author)
            await self.process_commands(message)


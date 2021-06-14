# Fix for Momo.close raising exceptions - Issue with Win 10
# https://github.com/Rapptz/discord.py/issues/5209
import platform
import asyncio
if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import functools
from datetime import datetime
import pytz

# ----------------------------------------------------------------------------

from discord.ext import commands
from lib.classes import User, Pack

class Momo(commands.Bot):
    
    def __init__(self, *args, database, **kwargs):
        self.db = database
        self.unpack_data()
        self.last_modified = datetime.utcnow()
        super().__init__(*args, **kwargs)


    @property
    def users(self):
        return self._users  


    def update_last_modified(self):
        self.last_modified = datetime.utcnow()


    def add_server(self, server):
        self.server = server

    
    def get_user_objects(self):
        user_dict_dict = self.db.data["users"]
        return { int(user_id): User(user_dict=user_dict, id=user_id) for user_id, user_dict in user_dict_dict.items() }


    def get_user_dicts(self):
        user_object_dict = self.users
        return { str(user_id): user_object.get_dict() for user_id, user_object in user_object_dict.items() }


    def get_pack_objects(self):
        pack_list_dict = self.db.data["packs"]
        return { pack_name: Pack(name=pack_name, pack_list=pack_list) for pack_name, pack_list in pack_list_dict.items() }


    def get_pack_lists(self):
        pack_object_dict = self.packs
        return { pack_name: pack_object.get_list() for pack_name, pack_object in pack_object_dict.items() }


    def get_all_cards(self):
        return functools.reduce(lambda x,y: x+y, dict(sorted(self.packs.items())).values(), [])


    def pack_data(self):
        self.db.data["config"] = self.config 
        self.db.data["users"] = self.get_user_dicts()
        self.db.data["packs"] = self.get_pack_lists()


    def unpack_data(self):
        self.config = self.db.data["config"]
        self._users = self.get_user_objects()
        self.packs = self.get_pack_objects()


    def add_cogs(self, cogs):
        for cog in cogs:
            self.add_cog(cog(self))


    def run(self, *args, **kwargs):
        print("Connecting to Discord... ", end="")
        super().run(*args, **kwargs)


    async def on_ready(self):
        await self.get_channel(self.db.data["config"]["default-channel"])\
            .send("✅ En línea")


    async def on_message(self, message):
        author = message.author
        if not author.bot:
            if author.id not in self.users:
                self.users[author.id] = User(user=author)
            await self.process_commands(message)

    
    async def on_command_error(self, ctx, exception):
        cmd = ctx.command
        if cmd is None:
            await ctx.send("❌ Comando no reconocido")
        else:
            await ctx.send(f"Uso correcto: `{cmd.name} {cmd.usage}`\n" +
                str(exception))


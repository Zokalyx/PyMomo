# Fix for Momo.close raising exceptions - Issue with Win 10
# https://github.com/Rapptz/discord.py/issues/5209
import platform
import asyncio
if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# ----------------------------------------------------------------------------

from discord.ext import commands

class Momo(commands.Bot):
    
    def __init__(self, *args, database, **kwargs):
        self.db = database
        super().__init__(*args, **kwargs)


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
        if not message.author.bot:
            await self.process_commands(message)



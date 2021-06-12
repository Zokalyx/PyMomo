from discord.ext.commands import Cog, command, group, is_owner
from lib.classes import User


class MomoBot(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def save(self, ctx):
        msg = await ctx.send("Guardando datos... ")
        self.bot.pack_data()
        self.bot.db.save()
        await msg.edit(content="Guardando datos... ✅")


    @command()
    async def exit(self, ctx):
        self.bot.db.save()
        print("Shutting down...")
        await self.bot.close()


    @command()
    async def test(self, ctx, *, name):
        await ctx.send(f"Hi, {name}")


    @command()
    @is_owner()
    async def debug(self, ctx, *args):
        # Async exec in python
        # https://stackoverflow.com/questions/44859165/#53255739
        exec("async def __ex(momo, ctx):\n    return "
            + " ".join(args).replace("\"", "'"))
        print(await locals()["__ex"](self.bot, ctx))

from lib.db.db import database as db
from discord.ext.commands import Cog, command, is_owner


class BotCommands(Cog):
    """Comandos relacionados al bot"""

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def save(self, ctx):
        """Guarda los datos"""
        msg = await ctx.send("Guardando datos... ")
        db.save()
        await msg.edit(content="Guardando datos... ✅")

    @command()
    async def exit(self, ctx):
        """Apaga el bot (solo admin)"""
        db.save()
        print("Shutting down...")
        await self.bot.close()

    @command()
    async def test(self, ctx, name):
        """ASD"""
        await ctx.send(f"Hi, {name}")

    @command()
    @is_owner()
    async def debug(self, ctx, *args):
        print(eval(" ".join(args)))
from discord.ext.commands import Cog, command, group, is_owner

class MomoInfo(Cog):

    def __init__(self, bot):
        self.bot = bot


    @command()
    async def asd(self, ctx):
        await ctx.send("No implementado")

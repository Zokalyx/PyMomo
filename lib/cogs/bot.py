from discord.ext.commands import Cog, command, group, is_owner
from lib.classes import User


class MomoBot(Cog):
    """Comandos relacionados a Momo"""

    def __init__(self, bot):
        self.bot = bot
        self.name = "momo"
        self.aliases = ["bot", "b", "momo"]


    @command()
    async def save(self, ctx):
        """guarda todos los datos"""
        msg = await ctx.send("Guardando datos... ")
        self.bot.pack_data()
        self.bot.db.save()
        await msg.edit(content="Guardando datos... ✅")


    @command()
    async def exit(self, ctx):
        """guarda todos los datos y apaga el bot"""
        msg = await ctx.send("Guardando datos y apagando...")
        self.bot.db.save()
        await msg.edit(content="Guardando datos y apagando... ✅")
        print("Shutting down...")
        await self.bot.close()


    @command()
    async def ping(self, ctx):
        """muestra la latencia del bot con Discord"""
        ping = round(1000*self.bot.latency)
        await ctx.send(f"Tengo {ping} ms de latencia")


    @command(usage="<prefijo>")
    async def prefix(self, ctx, prefix):
        """cambia el prefijo de los comandos"""
        cfg = self.bot.config
        cfg['prefixes'][str(ctx.guild.id)] = prfx
        await ctx.send(f"El prefijo para comandos ahora es `{prfx}`")


    @command(usage="<nombre>")
    async def test(self, ctx, *, name):
        await ctx.send(f"Hi, {name}")


    @command(usage="<código>")
    @is_owner()
    async def debug(self, ctx, *, code):
        """ejecuta código y muestra el resultado en la consola"""
        # Async exec in python
        # https://stackoverflow.com/questions/44859165/#53255739
        exec("async def __ex(momo, ctx):\n    "
            + code.strip().replace("\n", "\n    "))
        print(await locals()["__ex"](self.bot, ctx))

    
    @command(usage="<código>")
    @is_owner()
    async def do(self, ctx, *, code):
        """ejecuta código y muestra el resultado en Discord"""
        exec("async def __ex(momo, ctx):\n    return " + code)
        await ctx.send(await locals()["__ex"](self.bot, ctx))

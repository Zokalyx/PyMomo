from discord.ext.commands import Cog, command, is_owner


class MomoBot(Cog):
    """Comandos relacionados a Momo"""

    def __init__(self, bot):
        self.bot = bot
        self.name = "bot"
        self.aliases = ["bot", "b", "momo"]

#-------------------------------COMMANDS--------------------------------------

    @command()
    async def save(self, ctx) -> None:
        """guarda todos los datos"""
        msg = await ctx.send("Guardando datos... ")
        self.bot.pack_data()
        self.bot.db.save()
        await msg.edit(content="Guardando datos... ✅")

    @command()
    @is_owner()
    async def load(self, ctx) -> None:
        """carga todos los datos"""
        msg = await ctx.send("Cargando datos... ")
        self.bot.db.load()
        self.bot.unpack_data()
        self.bot.update_last_modified()
        await msg.edit(content="Cargando datos... ✅")

    @command()
    @is_owner()
    async def read(self, ctx) -> None:
        """carga todos los datos del archivo json"""
        msg = await ctx.send("Cargando datos desde JSON... ")
        self.bot.db.load_json()
        self.bot.unpack_data()
        self.bot.update_last_modified()
        await msg.edit(content="Cargando datos desde JSON... ✅")

    @command()
    @is_owner()
    async def write(self, ctx) -> None:
        """guarda todos los datos al archivo json"""
        msg = await ctx.send("Guardando datos en JSON... ")
        self.bot.db.save_json()
        self.bot.unpack_data()
        self.bot.update_last_modified()
        await msg.edit(content="Guardando datos en JSON... ✅")

    @command()
    async def exit(self, ctx) -> None:
        """guarda todos los datos y apaga el bot"""
        await self.bot.cogs["MomoVoice"].leave(None)
        msg = await ctx.send("Guardando datos y apagando...")
        self.bot.db.save()
        await msg.edit(content="Guardando datos y apagando... ✅")
        print("Shutting down...")
        await self.bot.close()

    @command()
    async def ping(self, ctx) -> None:
        """muestra la latencia del bot con Discord"""
        ping = round(1000*self.bot.latency)
        await ctx.send(f"Tengo {ping} ms de latencia")

    @command(usage="<prefijo>")
    async def prefix(self, ctx, prefix) -> None:
        """cambia el prefijo de los comandos"""
        cfg = self.bot.config
        cfg['prefixes'][str(ctx.guild.id)] = prefix
        await ctx.send(f"El prefijo para comandos ahora es `{prefix}`")

    @command(usage="<nombre>")
    async def test(self, ctx, *, name) -> None:
        await ctx.send(f"Hi, {name}")

    @command(usage="<código>")
    @is_owner()
    async def debug(self, ctx, *, code) -> None:
        """ejecuta código y muestra el resultado en la consola"""
        # Async exec in python
        # https://stackoverflow.com/questions/44859165/#53255739
        exec("async def __ex(momo, ctx):\n    "
             + code.strip().replace("\n", "\n    "))
        print(await locals()["__ex"](self.bot, ctx))

    @command(usage="<código>")
    @is_owner()
    async def do(self, ctx, *, code) -> None:
        """ejecuta código y muestra el resultado en Discord"""
        exec("async def __ex(momo, ctx):\n    return " + code)
        await ctx.send(await locals()["__ex"](self.bot, ctx))

    @command()
    @is_owner()
    async def update(self, ctx) -> None:
        """actualiza el tiempo de último cambio de datos"""
        self.bot.update_last_modified()
        await ctx.send("Última actualización: " + str(self.bot.last_modified))

    """
    @command()
    @is_owner()
    async def set(self, ctx, *, code):
        \"""Establece un valor de los datos de Momo\"""
        args = code.split()
        if len(args) < 3:
            await ctx.send("Pocos argumentos")
            return
        sanitized = []
        for arg in args:
            try:
                sanitized.append(int(arg))
            except ValueError:
                sanitized.append(arg)
        current = getattr(self.bot, sanitized[0])
        for arg in sanitized[1:-2]:
            current = current[arg]
        current[sanitized[-2]] = sanitized[-1]
    """

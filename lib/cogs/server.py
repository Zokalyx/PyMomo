from discord.ext.commands import Cog, command
from aiohttp import web
import server
from lib.web import env, add_static, set_env


class MomoServer(Cog):
    """Comandos relacionados a la página web"""

    def __init__(self, bot):
        self.name = "web"
        self.aliases = ["web", "server"]
        self.bot = bot
        self.server = server.HTTPServer(
            bot=self.bot,
            port=8000,
            host="0.0.0.0"
        )
        add_static(self)
        set_env(self.bot.db.on_cloud)
        self.bot.loop.create_task(self._start_server())


    async def _start_server(self):
        await self.bot.wait_until_ready()
        print("Done!")
        await self.server.start()


    @server.add_route(path="/", method="GET", cog="MomoServer")
    async def home(self, request):
        self.bot.pack_data()
        return web.Response(
            body=env.get_template("test.html").render(name="Fran"),
            content_type="html"
        )

    
    @command()
    async def link(self, ctx):
        """Muestra el link de la página web de Momo"""
        if self.bot.db.on_cloud:
            await ctx.send("https://pymomo.zokalyx.repl.co")
        else:
            await ctx.send("http://localhost:8000")

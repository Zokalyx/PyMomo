from discord.ext.commands import Cog, command
from aiohttp import web
import aiohttp_jinja2
import jinja2
import server
import json
from lib.web import env, add_static


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
        if self.bot.db.on_cloud:
            env.globals["SP"] = "https://pymomo.zokalyx.repl.co/"
        else:
            env.globals["SP"] = "http://localhost:8000/"
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

    """
    @server.add_route(path="/images/momo", method="GET", cog="MomoServer")
    async def static_momo(self, request):
        with open("./lib/web/images/momo.png", "rb") as m:
            img = m.read()
        return web.Response(
            body=img,
            content_type="image/png"
        )
    """

    
    @command()
    async def link(self, ctx):
        """Muestra el link de la página web de Momo"""
        if self.bot.db.on_cloud:
            await ctx.send("https://pymomo.zokalyx.repl.co")
        else:
            await ctx.send("http://localhost:8000")

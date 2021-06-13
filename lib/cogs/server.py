from discord.ext.commands import Cog, command
from aiohttp import web
import server
import json


class MomoServer(Cog):
    """Comandos relacionados a la página web"""

    def __init__(self, bot):
        self.name = "web"
        self.aliases = ["server"]
        self.bot = bot
        self.server = server.HTTPServer(
            bot=self.bot,
            port=8000,
            host="0.0.0.0"
        )
        self.bot.loop.create_task(self._start_server())


    async def _start_server(self):
        await self.bot.wait_until_ready()
        print("Done!")
        await self.server.start()


    @server.add_route(path="/", method="GET", cog="MomoServer")
    async def home(self, request):
        self.bot.pack_data()
        return web.json_response(
            data=self.bot.db.data,
            status=200
        )

    
    @command()
    async def link(self, ctx):
        """Muestra el link de la página web de Momo"""
        if self.bot.db.on_cloud:
            await ctx.send("https://")


from discord.ext.commands import Cog, command
from aiohttp import web
import server
from lib.web import env, set_env, was_modified, was_modified_static
import os
from datetime import datetime


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
        # add_static(self)
        set_env(self.bot.db.on_cloud)
        self.bot.loop.create_task(self._start_server())


    async def _start_server(self):
        await self.bot.wait_until_ready()
        print("Done!")
        await self.server.start()


    @server.add_route(path="/", method="GET", cog="MomoServer")
    async def home(self, request):
        if was_modified(self, request):
            return web.Response(
                body=env.get_template("home.html").render(),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
                }
            )
        else:
            return web.Response(status=304)


    @server.add_route(path="/packs/{pack}", method="GET", cog="MomoServer")
    async def home(self, request):
        if was_modified(self, request):
            self.bot.pack_data()
            pack = request.match_info["pack"]
            return web.Response(
                body=env.get_template("cards.html").render(cards=self.bot.packs[pack], pack=pack),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
                }
            )
        else:
            return web.Response(status=304)
    

    @server.add_route(path="/cards/", method="GET", cog="MomoServer")
    async def home(self, request):
        if was_modified(self, request):
            self.bot.pack_data()
            return web.Response(
                body=env.get_template("all.html").render(cards=self.bot.get_all_cards(), pack="Todas las cartas"),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
                }
            )
        else:
            return web.Response(status=304)


    @server.add_route(path="/packs/", method="GET", cog="MomoServer")
    async def home(self, request):
        if was_modified(self, request):
            self.bot.pack_data()
            return web.Response(
                body=env.get_template("packs.html").render(packs=self.bot.packs),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime("%a, %d %b %Y %H:%M:%S GMT")
                }
            )
        else:
            return web.Response(status=304)


    @server.add_route(path="/images/{file}", method="GET", cog="MomoServer")
    async def home(self, request):
        filename = request.match_info["file"]
        try:
            extension = filename[filename.index(".")+1:]
            mod_time = os.path.getmtime("./lib/web/images/" + filename)
            if was_modified_static(mod_time, request):
                with open("./lib/web/images/" + filename, "rb") as img:
                    return web.Response(
                        body=img.read(),
                        content_type="image/" + extension,
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(mod_time).strftime("%a, %d %b %Y %H:%M:%S GMT")
                        }
                    )
            else:
                return web.Response(status=304)
        except (FileNotFoundError, ValueError):
            print(f"404: Image {filename} not found!")
            return web.Response(
                body="No se encontró ese archivo",
                content_type="text/plain",
                status=404
            )

    
    @server.add_route(path="/fonts/{file}", method="GET", cog="MomoServer")
    async def home(self, request):
        filename = request.match_info["file"]
        try:
            extension = filename[filename.index(".")+1:]
            mod_time = os.path.getmtime("./lib/web/fonts/" + filename)
            if was_modified_static(mod_time, request):
                with open("./lib/web/fonts/" + filename, "rb") as img:
                    return web.Response(
                        body=img.read(),
                        content_type="font/" + extension,
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(mod_time).strftime("%a, %d %b %Y %H:%M:%S GMT")
                        }
                    )
            else:
                return web.Response(status=304)
        except (FileNotFoundError, ValueError):
            print(f"404: Image {filename} not found!")
            return web.Response(
                body="No se encontro ese archivo",
                content_type="text/plain",
                status=404
            )

    
    @server.add_route(path="/styles/{file}", method="GET", cog="MomoServer")
    async def home(self, request):
        filename = request.match_info["file"]
        try:
            mod_time = os.path.getmtime("./lib/web/styles/" + filename)
            if was_modified_static(mod_time, request):
                with open("./lib/web/styles/" + filename, "rb") as style:
                    return web.Response(
                        body=style.read(),
                        content_type="text/css",
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(mod_time).strftime("%a, %d %b %Y %H:%M:%S GMT")
                        }
                    )
            else:
                return web.Response(status=304)
        except FileNotFoundError:
            print(f"404: Stylesheet {filename} not found!")
            return web.Response(
                body="No se encontró ese archivo",
                content_type="text/plain",
                status=404
            )

    
    @server.add_route(path="/scripts/{file}", method="GET", cog="MomoServer")
    async def home(self, request):
        filename = request.match_info["file"]
        try:
            mod_time = os.path.getmtime("./lib/web/scripts/" + filename)
            if was_modified_static(mod_time, request):
                with open("./lib/web/scripts/" + filename, "rb") as style:
                    return web.Response(
                        body=style.read(),
                        content_type="text/script",
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(mod_time).strftime("%a, %d %b %Y %H:%M:%S GMT")
                        }
                    )
            else:
                return web.Response(status=304)
        except FileNotFoundError:
            print(f"404: Script {filename} not found!")
            return web.Response(
                body="No se encontró ese archivo",
                content_type="text/plain",
                status=404
            )

    
    @command()
    async def link(self, ctx):
        """Muestra el link de la página web de Momo"""
        if self.bot.db.on_cloud:
            await ctx.send("https://pymomo.zokalyx.repl.co")
        else:
            await ctx.send("http://localhost:8000")

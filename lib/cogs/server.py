import os
from datetime import datetime

import server
from aiohttp import web

from discord.ext.commands import Cog, command
from lib.web import env, set_env, was_modified, was_modified_static
from lib.cogs.webhelper import card_graph, user_graph, time_ago_formatter


class MomoServer(Cog):
    """Comandos relacionados a la página web"""

    def __init__(self, bot):
        self.name = "web"
        self.aliases = ["web", "server"]
        self.bot = bot
        self.server = server.HTTPServer(
            bot=self.bot,
            port=25565,
            host="0.0.0.0"
        )
        set_env(self.bot.db.on_cloud)
        self.bot.loop.create_task(self._start_server())

    async def _start_server(self) -> None:
        """Enciende el servidor http"""
        await self.bot.wait_until_ready()
        print("Done!")
        await self.server.start()

    @server.add_route(path="/", method="GET", cog="MomoServer")
    async def home(self, request) -> web.Response:
        """Momo webpage home screen"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            return web.Response(
                body=env.get_template("home.html").render(),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

# ---------------------------CARD RELATED-------------------------------------

    @server.add_route(path="/packs/", method="GET", cog="MomoServer")
    async def packs(self, request) -> web.Response:
        """Page for the selection of a pack to visualize"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            return web.Response(
                body=env.get_template("packs.html").render(
                    packs=self.bot.packs,
                    all_cards_amount=self.bot.get_all_cards()
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(path="/packs/{pack}/", method="GET", cog="MomoServer")
    async def pack(self, request) -> web.Response:
        """Page for the visualization of cards of a specific pack"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            pack = request.match_info["pack"]
            return web.Response(
                body=env.get_template("cards.html").render(
                    cards=self.bot.packs[pack],
                    pack=pack,
                    users=self.bot.users
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(path="/cards/", method="GET", cog="MomoServer")
    async def cards(self, request) -> web.Response:
        """Page for the visualization of all cards"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            return web.Response(
                body=env.get_template("all.html").render(
                    cards=self.bot.get_all_cards(),
                    pack="Todas las cartas",
                    users=self.bot.users
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(
        path="/packs/{pack}/{id}",
        method="GET",
        cog="MomoServer"
    )
    async def card(self, request) -> web.Response:
        """Page for a single card"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            match_info = request.match_info
            self.bot.pack_data()
            card = self.bot.packs[match_info["pack"]][int(match_info["id"])-1]
            user = self.bot.users[card.owner] if card.owner else None
            return web.Response(
                body=env.get_template("card.html").render(
                    card=card,
                    user=user,
                    users=self.bot.users,
                    custom_name=card.get_best_name(),
                    card_graph=card_graph(card),
                    obtained_time_ago=time_ago_formatter(card.stats["obtained"]["time"]),
                    roll_time_ago=time_ago_formatter(card.stats["last_roll"]["time"])
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

# ---------------------------USER RELATED-------------------------------------

    @server.add_route(path="/users/", method="GET", cog="MomoServer")
    async def users(self, request) -> web.Response:
        """Page for the selection of a user to visualize"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            full_collections = self.bot.get_full_collections()
            return web.Response(
                body=env.get_template("users.html").render(
                    users=self.bot.get_sorted_users(),
                    collections=full_collections
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(path="/users/{id}", method="GET", cog="MomoServer")
    async def user(self, request) -> web.Response:
        """Page for the visualization of a single user's data"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            user = self.bot.users[int(request.match_info["id"])]
            return web.Response(
                body=env.get_template("profile.html").render(
                    user=user,
                    collections=self.bot.get_full_collections(),
                    rarity_amounts=user.get_rarity_counts(),
                    rarity_proportions=user.get_rarity_counts(
                        proportion=True
                    ),
                    user_graph=user_graph(user),
                    top_cards=user.get_top(5),
                    total_value=user.get_total_value(),
                    config=self.bot.config
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(path="/collections/{id}/", method="GET", cog="MomoServer")
    async def packs(self, request) -> web.Response:
        """Page for the selection of a collection to visualize"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            user = self.bot.users[int(request.match_info["id"])]
            return web.Response(
                body=env.get_template("collection.html").render(
                    user=user,
                    collection=user.collection,
                    all_cards_amount=user.get_all_cards()
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(
        path="/collections/{id}/all",
        method="GET",
        cog="MomoServer"
    )
    async def allcollection(self, request) -> web.Response:
        """Page for visualizing all the cards of a user"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            user = self.bot.users[int(request.match_info["id"])]
            return web.Response(
                body=env.get_template("allcollection.html").render(
                    user=user,
                    cards=self.bot.get_full_collections()[user.id]
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(
        path="/collections/{id}/{pack}",
        method="GET",
        cog="MomoServer"
    )
    async def packcollection(self, request) -> web.Response:
        """Page for visualizing the cards of a user of a pack"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            user = self.bot.users[int(request.match_info["id"])]
            pack_name = request.match_info["pack"]
            return web.Response(
                body=env.get_template("packcollection.html").render(
                    pack=pack_name,
                    user=user,
                    cards=user.collection[pack_name]
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

# ------------------------------OTHER-----------------------------------------

    @server.add_route(path="/changelog/", method="GET", cog="MomoServer")
    async def changelog(self, request) -> web.Response:
        """Page for changelog"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            return web.Response(
                body=env.get_template("changelog.html").render(),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

    @server.add_route(path="/configuration/", method="GET", cog="MomoServer")
    async def config(self, request) -> web.Response:
        """Page for config"""
        # Only show content if there was any modifications since
        if was_modified(self, request):
            self.bot.pack_data()
            return web.Response(
                body=env.get_template("config.html").render(
                    odds=self.bot.get_odds()
                ),
                content_type="html",
                headers={
                    "Last-Modified": self.bot.last_modified.strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    )
                }
            )
        else:
            return web.Response(status=304)

# ------------------------------STATIC----------------------------------------

    @server.add_route(path="/images/{file}", method="GET", cog="MomoServer")
    async def image(self, request) -> web.Response:
        """Returns an image"""
        filename = request.match_info["file"]
        # Try returning if file exists
        try:
            extension = filename[filename.index(".")+1:]
            # Only return file if there was any change to the files
            mod_time = os.path.getmtime("./lib/web/images/" + filename)
            if was_modified_static(mod_time, request):
                with open("./lib/web/images/" + filename, "rb") as img:
                    return web.Response(
                        body=img.read(),
                        content_type="image/" + extension,
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(
                                mod_time
                            ).strftime("%a, %d %b %Y %H:%M:%S GMT")
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
    async def font(self, request) -> web.Response:
        """Returns a font file"""
        filename = request.match_info["file"]
        # Try returning if file exists
        try:
            extension = filename[filename.index(".")+1:]
            # Only return file if there was any change to the files
            mod_time = os.path.getmtime("./lib/web/fonts/" + filename)
            if was_modified_static(mod_time, request):
                with open("./lib/web/fonts/" + filename, "rb") as img:
                    return web.Response(
                        body=img.read(),
                        content_type="font/" + extension,
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(
                                mod_time
                            ).strftime("%a, %d %b %Y %H:%M:%S GMT")
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
    async def style(self, request) -> web.Response:
        """Returns a css file"""
        filename = request.match_info["file"]
        # Try returning if file exists
        try:
            mod_time = os.path.getmtime("./lib/web/styles/" + filename)
            # Only return file if there was any change to the files
            if was_modified_static(mod_time, request):
                with open("./lib/web/styles/" + filename, "rb") as style:
                    return web.Response(
                        body=style.read(),
                        content_type="text/css",
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(
                                mod_time
                            ).strftime("%a, %d %b %Y %H:%M:%S GMT")
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
    async def script(self, request) -> web.Response:
        """Returns a js file"""
        filename = request.match_info["file"]
        # Try returning if file exists
        try:
            mod_time = os.path.getmtime("./lib/web/scripts/" + filename)
            # Only return file if there was any change to the files
            if was_modified_static(mod_time, request):
                with open("./lib/web/scripts/" + filename, "rb") as style:
                    return web.Response(
                        body=style.read(),
                        content_type="text/script",
                        headers={
                            "Last-Modified": datetime.utcfromtimestamp(
                                mod_time
                            ).strftime("%a, %d %b %Y %H:%M:%S GMT")
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

# ----------------------------COMMANDS----------------------------------------

    @command()
    async def link(self, ctx):
        """Muestra el link de la página web de Momo"""
        if self.bot.db.on_cloud:
            await ctx.send("https://pymomo.zokalyx.repl.co")
        else:
            await ctx.send(f"http://localhost:{self.server.port}")

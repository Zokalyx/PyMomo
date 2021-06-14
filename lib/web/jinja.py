from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from aiohttp.web import Response
from server.server import RouteDef, _ROUTES
from datetime import timedelta, datetime
import pytz

env = Environment(
    loader=FileSystemLoader("./lib/web/templates"),
    autoescape=select_autoescape()
)


def set_env(on_cloud):
    if on_cloud:
        env.globals["SP"] = "https://pymomo.zokalyx.repl.co/"
    else:
        env.globals["SP"] = "http://localhost:8000/"


def was_modified(cog, req):
    try:
        req.if_modified_since
        return (
            pytz.UTC.localize(cog.bot.last_modified)
            - req.if_modified_since > timedelta(seconds=1)
        )
    except (AttributeError, TypeError):
        return True


def was_modified_static(mod_time, req):
    try:
        req.if_modified_since
        return (
            pytz.UTC.localize(datetime.utcfromtimestamp(mod_time))
            - req.if_modified_since > timedelta(seconds=1)
        )
    except (AttributeError, TypeError):
        return True



env.filters["pluralize"] = lambda x: "" if x == 1 else "s"

"""
def add_static(cog):
    for folder in ["images", "scripts", "styles", "fonts"]:
        folder_path = "./lib/web/" + folder + "/"
        for fil in os.listdir(folder_path):
            path = folder_path + fil
            file_name, file_extension = os.path.splitext(path)
            async def fuck(req, path=path, folder=folder, extension=file_extension[1:]):
                with open(path, "rb") as i:
                    body = i.read()
                if folder == "images":
                    content_type = "image/" + extension
                elif folder == "scripts":
                    content_type = "text/javascript"
                elif folder == "styles":
                    content_type = "text/css"
                elif folder == "fonts":
                    content_type = "font/" + extension
                return Response(body=body, content_type=content_type)
            _ROUTES.append(RouteDef(f"/{folder}/" + fil, "GET", fuck, cog))
            setattr(cog, folder + "_" + fil.replace(".", "_"), fuck)
"""

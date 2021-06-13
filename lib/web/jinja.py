from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("./lib/web/templates"),
    autoescape=select_autoescape()
)
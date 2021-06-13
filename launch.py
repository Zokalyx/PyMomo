import os
import dotenv
dotenv.load_dotenv("./.env")

from lib.db import Database
from lib.bot import Momo, init_dict
from lib.cogs import cogs

db = Database(on_cloud=bool(int(os.getenv("ON_CLOUD"))))
db.load()

momo = Momo(database=db, **init_dict)
momo.add_cogs(cogs)
momo.run(os.getenv("PYMOMO_TOKEN"))

from flask import Flask

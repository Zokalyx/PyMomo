import os
import dotenv
dotenv.load_dotenv("./.env")

from lib.db import Database
from lib.bot import Momo, init_dict

db = Database(on_cloud=bool(int(os.getenv("ON_CLOUD"))))
db.load()

momo = Momo(data=db.content, **init_dict)
momo.run(os.getenv("PYMOMO_TOKEN"))

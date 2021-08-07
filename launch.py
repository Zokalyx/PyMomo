import os
import asyncio
import websockets
import dotenv
dotenv.load_dotenv("./.env")

from lib.db import Database
from lib.bot import Momo, init_dict
from lib.cogs import cogs

db = Database(on_cloud=bool(int(os.getenv("ON_CLOUD"))))
db.load()

async def response(websocket, path):
    print("Connection established")
    while True:
        recv = await websocket.recv()
        print(recv)
        await websocket.send(recv)
        if recv == "Escape":
            break
    print("Connection closed")

server = websockets.serve(response, '0.0.0.0', '80')
asyncio.get_event_loop().run_until_complete(server)

momo = Momo(database=db, **init_dict)
momo.add_cogs(cogs)
momo.run(os.getenv("PYMOMO_TOKEN"))

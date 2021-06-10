from os import getenv
from dotenv import load_dotenv
import discord

load_dotenv("./.env")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run(getenv("PYMOMO_TOKEN"))

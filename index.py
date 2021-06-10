from os import getenv
from dotenv import load_dotenv
import discord

# Load .env variables
load_dotenv("./.env")

# Import replit if on cloud
if not int(getenv("LOCAL")):
    from replit import db

# Momo class
class Momo(discord.Client):
    async def on_ready(self):
        print('Logged in!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

# Initialize momo
momo = Momo()

# Connect to Discord
client.run(getenv("PYMOMO_TOKEN"))

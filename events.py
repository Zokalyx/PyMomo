import discord as ds
from database import *

async def on_message(message: ds.Message):
    if (not message.author.bot and
            message.content.startswith(config["prefix"])):
        await message.channel.send("Hola")
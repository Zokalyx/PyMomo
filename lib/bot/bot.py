from discord.ext.commands import Bot as Momo, UserInputError as err
from lib.db.db import database as db

# Hacky fix for momo.close() raising exceptions - Issue with Win 10
# https://github.com/Rapptz/discord.py/issues/5209
import platform
import asyncio
if platform.system() == 'Windows':
	asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# Helper function to be passed as argument to __init__ of Bot
def determine_prefix(bot, msg):
    cfg = db.content["config"]
    try:
        return cfg["prefixes"][str(msg.guild.id)]
    except KeyError:
        return cfg["default-prefixes"]


# Instance of bot
momo = Momo(command_prefix=determine_prefix)


# ---- Events ----
@momo.event
async def on_ready():
    print("Done!")

@momo.event
async def on_message(message):
    await momo.process_commands(message)

@momo.event
async def on_command_error(ctx, error):
    print(error)
    print(dir(error))
    cmd = str(ctx.command)
    if cmd == "debug":
        res = "❌ Error"
    else:
        if cmd in db.content["help"]:
            res = f"❌ Uso correcto de `{cmd}`: " + \
                db.content["help"][cmd]
        else:
            res = f"❌ No existe el comando `{cmd}`"
    await ctx.channel.send(res)


# ---- Commands ----
@momo.command()
async def save(ctx):
    msg = await ctx.channel.send("Guardando datos... ")
    db.save()
    await msg.edit(content="Guardando datos... ✅")

@momo.command()
async def exit(ctx):
    db.save()
    print("Shutting down...")
    await momo.close()

@momo.command()
async def test(ctx, name):
    await ctx.channel.send(f"Hi, {name}")

@momo.command()
async def debug(ctx, *args):
    print(eval(" ".join(args)))

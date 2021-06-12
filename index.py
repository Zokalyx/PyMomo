
import os
import dotenv

from discord.ext.commands import Bot, HelpCommand
import discord as ds

from lib.db.db import database as db
from lib.cogs import bot
cogs = [bot.BotCommands]




# Main function
def main():
    print("-------- PyMomo Alpha --------\n")

    # Load .env variables
    dotenv.load_dotenv("./.env")

    # Load database
    db.on_cloud = bool(int(os.getenv("ON_CLOUD")))
    db.load()

    # Initialize momo and add cogs
    momo = Bot(
        activity=ds.Activity(
            name="sugerencias",
            type=ds.ActivityType.listening
        ),
        status=ds.Status("dnd"),
        command_prefix=custom_command_prefix,
        help_command=custom_help_command,
        owner_id=284696251566391296
    )
    for cog in cogs:
        momo.add_cog(cog(momo))

    # Set event listeners for momo
    @momo.event
    async def on_ready():
        await momo.get_channel(db.content["config"]["default-channel"])\
            .send("Ready!")
        print("Done!")

    @momo.event
    async def on_message(message):
        await momo.process_commands(message)

    @momo.event
    async def on_command_error(ctx, error):
        print(error.args)
        print(f"Error: {error}")
        if cmd == "debug":
            res = "❌ Error"
        else:
            if cog is None:
                res = f"El comando `{cmd}` no está registrado"
            else:
                cmd = ctx.command
                res = f"Uso correcto de `{cmd.name}`: {cmd.description}"
        await ctx.send(res)

    # Run bot
    print("Connecting to Discord... ", end="")
    momo.run(getenv("PYMOMO_TOKEN"))


# Helper objects to be passed as arguments to __init__ of Bot
def custom_command_prefix(bot, msg):
    cfg = db.content["config"]
    try:
        return cfg["prefixes"][str(msg.guild.id)]
    except KeyError:
        return cfg["default-prefixes"]

def custom_command_not_found(cmd):
    return f"No existe el comando `{cmd}`"

custom_help_command = HelpCommand(
    command_not_found=custom_command_not_found
)

   
asd

# Execute
if __name__ == "__main__":
    main()

from os import getenv
from dotenv import load_dotenv
import discord
import events
import database as db

# Load .env variables
load_dotenv("./.env")

# True: deployed. False: debug/local
on_cloud = bool(int(getenv("ON_CLOUD")))

# Import replit if on cloud
if on_cloud:
    from replit import db

# Initialize momo
momo = discord.Client()


# Main function
def main() -> None:
    # Load database
    load_db(on_cloud)

    # Connect to Discord and run bot
    print("Connecting to Discord... ", end="")
    momo.run(getenv("PYMOMO_TOKEN"))


# Event handlers
@momo.event
async def on_ready():
    print("Success!")

@momo.event
async def on_message(message):
    await events.on_message(message)

@momo.event
async def on_reaction_add(reaction, user):
    print(f"Reaction from {user}: {reaction}")


def load_db(on_cloud: bool):
    if on_cloud:
        # TODO: Load replit database
        pass
    else:
        # TODO: Load local database
        pass

    return NotImplemented



# Execute
if __name__ == "__main__":
    main()

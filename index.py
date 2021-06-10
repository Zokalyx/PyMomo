from os import getenv
from dotenv import load_dotenv
import discord

# Load .env variables
load_dotenv("./.env")

# Import replit if on cloud, else, load local db
if int(getenv("LOCAL")):
    from replit import db
else:
    # TODO: Load local database


# Main function
def main():

    # Initialize momo
    momo = Momo()

    # Connect to Discord
    momo.run(getenv("PYMOMO_TOKEN"))


# Momo class
class Momo(discord.Client):
    async def on_ready(self):
        print('Logged in!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))


# Execute
if __name__ == "__main__":
    main()

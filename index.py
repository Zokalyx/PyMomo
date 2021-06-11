from os import getenv
import dotenv

from lib.db.db import database as db
from lib.bot.bot import momo


# Main function
def main():
    print("-------- PyMomo Alpha --------\n")

    # Load .env variables
    dotenv.load_dotenv("./.env")

    # Load database
    setattr(db, "on_cloud", bool(int(getenv("ON_CLOUD"))))
    db.load()

    # Run momo
    print("Connecting to Discord... ", end="")
    momo.run(getenv("PYMOMO_TOKEN"))


# Execute
if __name__ == "__main__":
    main()

import json
try:
    from replit import db as replitdb
except ModuleNotFoundError:
    pass


class Database:
    """Class that contains methods to read and write data, as well as an
    internal storage for it"""

    def __init__(self, on_cloud):
        self.on_cloud = on_cloud

    def load(self) -> None:
        """Loads data, either from replit or json"""
        print("Loading from database... ", end="")
        if self.on_cloud:
            self.data = json.loads(replitdb["data"])
        else:
            self.load_json()
        print("Done!")

    def load_json(self) -> None:
        """Loads data from json"""
        with open("./data/db.json", "r", encoding="utf-8") as database:
            self.data = json.loads(database.read())

    def save(self) -> None:
        print("Saving to database... ", end="")
        if self.on_cloud:
            replitdb["data"] = json.dumps(self.data, indent=4, sort_keys=True)
        else:
            self.save_json()
        print("Done!")

    def save_json(self) -> None:
        with open("./data/db.json", "w", encoding="utf-8") as database:
            database.write(json.dumps(self.data, indent=4, sort_keys=True))

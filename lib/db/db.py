import json
try:
    from replit import db as replitdb
except ModuleNotFoundError:
    pass


class Database:

    def __init__(self, on_cloud):
        self.on_cloud = on_cloud


    def load(self):
        print("Loading from database... ", end="")
        if self.on_cloud:
            pass
        else:
            with open("./data/db.json", "r", encoding="utf-8") as database:
                self.content = json.loads(database.read())
        print("Done!")


    def save(self):
        print("Saving to database... ", end="")
        if self.on_cloud:
            pass
        else:
            with open("./data/db.json", "w", encoding="utf-8") as database:
                database.write(json.dumps(self.content))
        print("Done!")

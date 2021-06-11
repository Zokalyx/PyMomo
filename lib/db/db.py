# Try importing replit database module, else import json for local db
try:
    from replit import db
except ModuleNotFoundError:
    import json

# Data class, contains functionality for loading and saving to/from database
class Database:

    # True if deployed, False if debug
    def set_cloud(self, on_cloud):
        self.on_cloud = on_cloud

    # Loads data either from replit or json
    def load(self):
        print("Loading from database... ", end="")
        if self.on_cloud:
            pass
        else:
            # Unpack loaded content
            with open("./data/db.json", "r", encoding="utf-8") as database:
                self.content = json.loads(database.read())
        print("Done!")


    # Save data either to replit or json
    def save(self):
        print("Saving to database... ", end="")
        if self.on_cloud:
            pass
        else:
            with open("./data/db.json", "w", encoding="utf-8") as database:
                database.write(json.dumps(self.content))
        print("Done!")





# Data variable that holds everything
database = Database()

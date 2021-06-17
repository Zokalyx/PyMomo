from lib.classes.collection import Collection

class User:

    def __init__(self, user=None, user_dict=None, id=None, packs=None):
        self.collection = {}
        if user_dict is None:
            self.default_name = user.display_name
            self.nicks = [user.name]
            self.img = str(user.avatar_url)
            self.color = user.color.value
            self.id = user.id
            for pack_name in packs:
                self.collection[pack_name] = Collection(name=pack_name, owner=self.id)
        else:
            for attr in user_dict:
                setattr(self, attr, user_dict[attr])
            self.id = id
            for pack_name, pack in packs.items():
                self.collection[pack_name] = Collection(
                    name=pack_name,
                    owner=self.id,
                    card_object_list=self.get_owned_cards_in(pack)
                )


    def get_dict(self):
        return { key: value for key, value in vars(self).items() if key not in ("id", "collection") }


    def get_owned_cards_in(self, pack):
        return [ card for card in pack if card.owner == self.id ] 

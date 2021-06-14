class Card():

    def __init__(self, *, link=None, id=None, pack=None, card_dict=None):
        if card_dict is None:
            self.link = link
        else:
            for attr in card_dict:
                setattr(self, attr, card_dict[attr])
        self.id = id
        self.pack = pack


    def get_dict(self):
        return {key: value for key, value in vars(self).items() if key not in ("id", "pack")}

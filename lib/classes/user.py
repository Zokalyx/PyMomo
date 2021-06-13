import discord as ds

class User:

    def __init__(self, user=None, user_dict=None):
        if user_dict is None:
            self.default_name = user.display_name
            self.nicks = [user.name]
            self.img = str(user.avatar_url)
            self.color = user.color.value
        else:
            for attr in user_dict:
                setattr(self, attr, user_dict[attr])


    def get_dict(self):
        return vars(self)

    


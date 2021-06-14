class User:

    def __init__(self, user=None, user_dict=None, id=None):
        if user_dict is None:
            self.default_name = user.display_name
            self.nicks = [user.name]
            self.img = str(user.avatar_url)
            self.color = user.color.value
            self.id = user.id
        else:
            for attr in user_dict:
                setattr(self, attr, user_dict[attr])
            self.id = id


    def get_dict(self):
        return {key: value for key, value in vars(self).items() if key != "id"}

    


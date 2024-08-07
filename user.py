from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    @staticmethod
    def get(user_id):
        if user_id in User.users:
            return User(user_id)
        return None
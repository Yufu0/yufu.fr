from bcrypt import hashpw, gensalt, checkpw
from flask_login import UserMixin
from bson import ObjectId

from . import mongo


class User(UserMixin):
    def __init__(self, username, email, password_hash, id=None):
        self.id: str = id
        self.username: str = username
        self.email: str = email
        self.password_hash: str = password_hash

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"

    def check_password(self, password) -> bool:
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @staticmethod
    def get(username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(user_data['username'], user_data['email'], user_data['password_hash'], str(user_data['_id']))
        return None

    @staticmethod
    def create(username, email, password):
        if mongo.db.users.find_one({'username': username}):
            return None
        password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
        mongo.db.users.insert_one({'username': username, 'email': email, 'password_hash': password_hash})
        return User.get(username)

    @staticmethod
    def get_by_id(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data['username'], user_data['email'], user_data['password_hash'], str(user_data['_id']))
        return None

from flask import Flask
from pymongo import MongoClient
from flask_login import LoginManager

from dotenv import load_dotenv
import os

# load_dotenv() loads environment variables from a .env file into the environment
load_dotenv()

# Create a Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['DEBUG'] = True

# Create a MongoDB client
username = os.getenv('MONGO_INITDB_ROOT_USERNAME')
password = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
hostname = os.getenv('MONGO_HOSTNAME')
port = os.getenv('MONGO_PORT')
database_name = os.getenv('MONGO_DATABASE_NAME')

print(f"mongodb://{username}:{password}@{hostname}:{port}/")
mongo = MongoClient(f"mongodb://{username}:{password}@{hostname}:{port}/")
mongo.db = mongo[database_name]


def create_app() -> Flask:
    create_database()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth/')

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = User.get_by_id(user_id)
        return user

    return app


def create_database():
    """Create the database if it doesn't exist"""
    if "users" not in mongo.db.list_collection_names():
        mongo.db.create_collection("users")
        print("Created Users Collection")

from . import database
from flask_login import UserMixin

class Note(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.String(1000))
    date = database.Column(database.DateTime(timezone=True), default=database.func.now())
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))

class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(30), unique=True)
    email = database.Column(database.String(50))
    password = database.Column(database.String)
    notes = database.relationship('Note')
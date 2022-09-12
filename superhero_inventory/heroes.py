from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

# Import for Secrets Module (Given by Python)
import secrets

# Imports for Login Manager
from flask_login import UserMixin

# Import for Flask Login
from flask_login import LoginManager

# Import for Flask-Marshmallow
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self,length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'



class Superhero(db.Model):
    id = db.Column(db.Integer, primary_key = True) # Creating a few columns for the database
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    comics = db.Column(db.Integer)
    power = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, content, name, description, comics, power, date_created, owner, user_token, id = ''):
        self.id = self.set_id()
        self.content = content
        self.name = name
        self.description = description
        self.comics = comics
        self.power = power
        self.date_created = date_created
        self.owner = owner
        self.user_token = user_token


    def __repr__(self):
        return f'The following Hero has been added: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())


# Creation of API Schema via the Marshmallow Object
class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'content','name', 'description', 'comics', 'power', 'date_created', 'owner']


hero_schema = HeroSchema()
heros_schema = HeroSchema(many = True)
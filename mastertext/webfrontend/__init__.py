from mastertext.settings import Config
from flask_misaka import Misaka
from flask import Flask
from playhouse.flask_utils import FlaskDB
from peewee import *
from flask_login import LoginManager
from mastertext.models import *

app = Flask(__name__)
Misaka(app)
app.config.from_object(Config)
app.db = FlaskDB(app)
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return NewUser.get(NewUser.id == id)


# @app.before_first_request
# def create_user():
#    for Model in (Role, User, UserRoles):
#        Model.drop_table(fail_silently=True)
#        Model.create_table(fail_silently=True)
#
#    user_datastore.create_user(email='matt@piusbird.space', password='password')

from . import routes
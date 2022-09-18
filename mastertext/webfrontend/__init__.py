from flask_misaka import Misaka
from flask import Flask
from flask_peewee.db import Database
from peewee import *
from flask_security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required
from mastertext.models import *

app = Flask(__name__)
Misaka(app)
from mastertext.settings import Config
app.config.from_object(Config)
db = Database(app)

from . import routes
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)


@app.before_first_request
def create_user():
    for Model in (Role, User, UserRoles):
        Model.drop_table(fail_silently=True)
        Model.create_table(fail_silently=True)
    
    user_datastore.create_user(email='matt@piusbird.space', password='password')

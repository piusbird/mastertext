"""
mastertext.webfrontend is a flask web frontend to TextObjectStore
and friends
"""

from flask_misaka import Misaka
from flask import Flask
from playhouse.flask_utils import FlaskDB
from flask_login import LoginManager
from mastertext.models import NewUser
from mastertext.singleton import BorgCache
from mastertext.settings import Config


app = Flask(__name__)
Misaka(app)
app.config.from_object(Config)
app.cache = BorgCache()
app.db = FlaskDB(app)
login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(uid):
    return NewUser.get(NewUser.id == uid)


from . import routes # noqa

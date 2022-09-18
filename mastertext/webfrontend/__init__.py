from flask_misaka import Misaka
from flask import Flask
app = Flask(__name__)
Misaka(app)
from mastertext.settings import Config
app.config.from_object(Config)

from . import routes
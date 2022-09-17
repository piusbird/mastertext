from flask_misaka import Misaka
from flask import Flask
app = Flask(__name__)

Misaka(app)
from . import routes
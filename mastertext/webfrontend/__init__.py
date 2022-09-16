from flask import Flask
app = Flask(__name__)
from flask_misaka import Misaka
Misaka(app)
from mastertext.webfrontend import routes

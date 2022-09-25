import gevent
from mastertext.importer import fetch_and_parse
from mastertext.singleton import BorgCache, StoreConnect
from mastertext.utils import MasterTextError
from flask import g
from flask import flash
from mastertext.webfrontend import app
from mastertext.models import Error
from datetime import datetime


def import_task(url):
    gevent.idle()

    ts = StoreConnect().get_objstore()

    with app.app_context():
        try:
            text = fetch_and_parse(url)
            ts.create_object(text)
        except MasterTextError as e:
            Error.create(date=datetime.now(), message=str(e))


def flush_cache():
    bc = BorgCache()
    bc.cache = {}
    gevent.spawn_later(1800, flush_cache)

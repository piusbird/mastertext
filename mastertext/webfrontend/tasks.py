import gevent
from mastertext.importer import fetch_and_parse
from mastertext.singleton import BorgCache, StoreConnect



def import_task(url):
    gevent.idle()
    ts = StoreConnect().get_objstore()
    text = fetch_and_parse(url)
    ts.create_object(text)

def flush_cache():
    bc = BorgCache()
    bc.cache =  {}
    gevent.spawn_later(1800, flush_cache)
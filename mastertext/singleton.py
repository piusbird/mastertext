# We wrap the database and TextObjectStore connections in a borg singleton 
# for now because we don't want the web app spawning more than one connection to 
# the db for data integraty reasons. This is an ugly HAX. To work around some 
# file system and SQLite issues
from mastertext.objectstore import TextObjectStore
class StoreConnect(object):
    _shared_borg_state = {}

    def __new__(cls, *args, **kwargs):
	    obj = super(StoreConnect, cls).__new__(cls, *args, **kwargs)
	    obj.__dict__ = cls._shared_borg_state
	    return obj
    
    def __init__(self):

        self.ObjectStoreConnect = TextObjectStore()

    def get_objstore(self):
        return self.ObjectStoreConnect


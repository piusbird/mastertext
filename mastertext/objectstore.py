# MasterText Object store main class and utility functions
import re
from datetime import datetime
import peewee
from collections import ChainMap
from socket import gethostname
from mastertext.models import *
from mastertext.utils import MasterTextError, sha1_id_object

# Confession time the only reason this is not written in Haskell is I needed it yesterday
# And I'm out of practice but there will be lambdas and monads and all that sort of stuff all over
# this. Deal with it!
# this function will return True if the string matches a valid distinctive sha-1 hash
# The 7 char limit might need to be revisited at some point. But if I run into that bug
# I'll be happy


def valid_hash(h): return bool(re.match('^[0-9a-f]{7,40}$', h))


def unpack(u): return None if len(u) < 1 else u[0]


class ObjectNotFoundError(MasterTextError):
    pass


class MalformedHashError(ObjectNotFoundError):
    pass


class TextObjectStore:

    def retrieve_object(self, phash, attribs=False):

        if not valid_hash(phash):
            raise MasterTextError("Not a hash")

        hashin = phash + '%'  # sqlite wildcard
        hrows = [r for r in Link.select().where(Link.phash ** hashin)]

        if len(hrows) > 1:
            raise MasterTextError("Hash indistinct")
        lh = unpack(hrows)
        if lh is None or lh.count < 1:  # this should short circut if unpack returns None
            raise ObjectNotFoundError(phash + " Not found")
        textobj = unpack(Hive.select().where(Hive.hashid == lh.phash).dicts())
        if textobj is None:
            raise ObjectNotFoundError("Orphened Reference")
        return textobj if attribs else textobj['data']

    @database.atomic('IMMEDIATE')
    def create_object(self, data, *args, orphen=False, **kwargs):
        newhash = sha1_id_object(data)
        try:
            lh = Link.create(phash=newhash, count=1)
        except peewee.IntegrityError:
            lh = Link.get(Link.phash == newhash)
            lh.count += 1
            lh.save()
            if not orphen:
                return {'hash': lh.phash, 'count': lh.count}

        defaults = {'hashid': lh.phash, 'data': data, 'inject_date': str(
            datetime.now()), 'orighost': gethostname()}
        combined = ChainMap(kwargs, defaults)
        final = dict(combined)
        newobj = Hive.create(**final)
        newobj.save()
        return {'hash': lh.phash, 'count': lh.count}

    def search_text(self, ftsterm):

        q = Hive.search_bm25(ftsterm)
        results = [r.hashid for r in q]
        return {'count': len(results), "ids": results}

    @database.atomic('IMMEDIATE')
    def destroy_object(self, hashid):
        try:
            lh = Link.get(phash=hashid)
            oldcount = lh.count
            q = Hive.delete().where(Hive.hashid == lh.phash)
            q.execute()
            lh.delete_instance()
            return {'hash': hashid, 'count': -oldcount}
        except:
            return {'hash': hashid, 'count': -1}

    @database.atomic('IMMEDIATE')
    def delete_object(self, hashid):

        try:
            lh = Link.get(phash=hashid)
            lh.count -= 1
            lh.save()
            oldcount = lh.count 
            if lh.count < 1:
                self.destroy_object(lh.phash)
            return {'hash': hashid, 'count': oldcount}
        except:
            return {"hash": hashid, "count": -1}

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


def valid_hash(h):
    """
    Will return true if the string h is a valid hexdigest of an SHA-1 Hash
    This will accept shortened hashes al-la git with the lower limit set to 7 chars
    """
    return bool(re.match('^[0-9a-f]{7,40}$', h))


def unpack(u):
    """
    Returns the first item in a collection/contianer  or None if len(u) < 1.
    peewee insists on returning things in collections even if there is only one thing retreived
    as their often is with this program. This function saves you from writing obscure expresions 
    all over the place.
    """
    return None if len(u) < 1 else u[0]


class ObjectNotFoundError(MasterTextError):
    pass


class MalformedHashError(ObjectNotFoundError):
    pass


class TextObjectStore:
    """
    The TextObjectStore is the heart of MasterText
    It is a content addressable, deduplicating, full text searchable
    store of free form text documents. The main API does not include support for 
    advanced features such as tags, notes and bookmarks. Those will be implemented 
    by later APIs.

    The TextObjectStore assigns every document given to it for storage, a unique identifer
    based upon the content of the text, and some additional data.
    If a subsequent docuement has the same identifier 
    The store will not store a duplicate copy of the text. A reference counter will be incremented
    instead. This ensures both content addressiblity, and deduplication
    """

    def retrieve_object(self, phash, attribs=False):
        """
        Given a valid_hash(phash) this method will return the document 
        stored with that idenifer, as a unicode string.
        Setting attribs to True will return a dictionary contianing the document data
        and all metadata on the document stored in the Hive.

        Will raise MasterTextError under two conditions
        1. If not valid_hash(phash)
        2. If the hash or abbrivation given has more than one possible document
            This can happen in the case of database coruption, 
            or if the database contains more than 2^16 objects.
            in either event this should be reported.

        Will raise ObjectNotFoundError under two conditons
        1. No such document exists
        2. The document's identifer exists im the reference counter but not in the hive
            Usually this happens due to a delete operation being in progress at request time  
        """

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
        """
        Creates and stores a document object
        Takes the data to be stored as a utf-8 string.
        Also accepts any values that the Hive model accepts
        and will use those in place of defaults
        NB: Hive cannot data type constriants so be careful 
        when setting those values manually

        Also accepts the keyword bool orphen which will bypass reference counter checks
        and store an object in the hive regardless of weather or not it already exists.
        This is useful for both fixing and causing errors. But should not be needed in 
        normal operation.

        Returns a dict contianing the documents hash-id, and the current 
        value of reference counter.

        Will raise a type error if data to be injected is not text  
        """
        newhash = sha1_id_object(data)
        try:
            lh = Link.create(phash=newhash, count=1)
        except peewee.IntegrityError:
            lh = Link.get(Link.phash == newhash)
            lh.count += 1
            lh.save()
            Hive.update(inject_date=str(datetime.now())
                        ).where(Hive.hashid == newhash)
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
        """
        Perform a full text search of the database
        Using the bm25 ranking algorithm.
        Accepts an Sqlite FTS5 expression as ftstem
        Returns a dict contianing a count of the number of results
        and ids a list of the hash-id's of the matching documents
        for use with other api functions.

        No exceptions are raised 
        """

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

    def sample_object(self, hashid):
        o = self.retrieve_object(hashid)
        return o[0:399]

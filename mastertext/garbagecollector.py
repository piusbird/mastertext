"""
 MasterText Garbage Collector
We Intened to build a content addressable file system from our Database schema;
but you cannot enforce PRIMARY KEY constriants on a full text searchable table
Thus in testing on V0 database duplicates were injected.

Allowing duplicates expands the size of the on disk database by almost double,
slows down search by a factor of 4 at least, and prevents us from using the
full power of a KV store.

To solve this we do two things we create the LinkTable see models.Links,
and forbid the creation of duplicate objects from the API
But we still need a garbage collector, and deduplicator

So we build a mark/sweep dedup; Kinda sorta if you squint **really** hard

This algorithm is likely O(n^2) in worst case. However the program should not
create records in a way that leaves much garbage going forward.
So it should only invoke worst case performance on rare occisions.
"""

import peewee
from mastertext.models import Link, Hive


def dedup_mark(hashlist):

    dups_li = []
    for h in hashlist:
        print("Dedup on " + h)
        q = Hive.select(Hive.rowid).where(Hive.hashid == h)
        possible = [int(str(r)) for r in q]  # noqa
        if len(possible) > 1:
            dups_li.append((h, possible))

    return dups_li


def dedup_sweep(marks):

    destuction = []
    for m in marks:
        (hid, rows) = m
        try:
            Link.create(phash=hid, count=len(rows))
        except peewee.IntegrityError:
            lk = Link.get(phash=hid)
            if lk.count <= len(rows):
                lk.count += len(rows) - lk.count
            else:
                # We should not get here
                # TODO: This else is an error means
                # that the refernce counter has gone bad
                # the usual way of solving this is to walk the b-trees
                # and refresh the counter from that but as this is treeless
                # I got nothing setting the counter to 1 avoids data loss
                # so would aborting the write, my instinct tells me to set it to 1 so
                # that's what we'll do, and if I'm wrong we'll change it
                lk.count = 1
            lk.save()
        destuction.extend(rows[1:])
    return destuction


def gc_mark_sweep():
    q = Link.select(Link.phash).where(Link.count < 1)
    destroy = [str(r) for r in q]  # noqa
    return destroy


def gc_dealloc(items):

    for i in items:
        q = Hive.delete().where(Hive.hashid == i)
        q.execute()
        goodbye = Link.delete().where(Link.phash == i)
        goodbye.execute()


def dedup_dealloc(items):

    for i in items:
        print("Delete ", i)
        q = Hive.delete().where(Hive.rowid == i)
        q.execute()

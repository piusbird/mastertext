# queries.py common querys for MasterText, and other utility functions

import sqlite3
import hashlib
import os
import socket

"""
Please don't use any of the stuff in this file or subpackage
It was part of the pre alpha version of this program
and manipulates a version 0 database
Version 0 databases suck but as the main production user
of this 2am special has a 4GB V0 database that's not going anywhere
we need to keep this code around in case we need it later

There is a life lesson herein and that is to **always** THINK then CODE
"""


SAMPLE_SIZE = 1024
ijqs = "INSERT INTO hive VALUES (?,?,?,?)"

# Every text in this database has a id
# that's uniqueish. The id is the blake2b
# hexdigest of the first 1024 characters
# of the text, Or the hash of the full text
# if TEXT > 1K.
#
# NB: We don't enforce a constriant using it
# I.E two or more texts May have the same id value
# But we don't want that to happen too often
# The only reason it should happen is if the texts concerned
# are either identical to or variants of one another
# hence the 1k sample size


def insert_text(dbc, text):

    ourhost = os.getenv("mt_host", socket.gethostname())
    ds = datetime.now().strftime("%F")
    try:
        buf = text.decode("utf-8")
    except UnicodeDecodeError as e:
        buf = text.decode("iso-8859-1").encode("utf8")

        c = dbc.cursor()
        hashid = sample_buffer(buf)
        c.execute(ijqs, (hashid, ds, ourhost, buf))
        return hashid


# The Old id generator
# Wrote it before i knew what i was doing
# in a 2am coding binge
# It turns out blake2 is really really bad for the purpose
# and using sha1 like everybody else
# with a 1k sample results in more collisions
# then i wanted

# so we will have to ditch the collision plan
# and implement diff/compare properly when we need it
def old_id_gen(buf):

    m = hashlib.blake2b()
    smpEnd = SAMPLE_SIZE - 1
    sample = buf if len(buf) < SAMPLE_SIZE else buf[0:smpEnd]
    try:
        m.update(sample.encode("utf-8"))
    except:
        clean = sample.decode("iso-8859-1")
        m.update(clean.encode("utf-8"))

    return m.hexdigest()

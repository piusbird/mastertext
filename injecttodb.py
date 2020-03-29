#!/usr/bin/env python3
# Database injector for MasterText
# Matt Arnold 2020
# Warning this is very very rough
# but it does work

import sys
import os
import hashlib
import sqlite3
import socket
from datetime import datetime
from mastertext.common import *
# We assume that if the database file already
# exists then the proper schema is in place
# I might wanna fix that sooner or later
# if this product has any non me consumers
# but as that isn't true right now
# I'll just deal with the pile of
# exceptions that will happen
# if we connect to the wrong db, as i consider it a feature

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

def sample_buffer(buf):

    m = hashlib.blake2b()
    smpEnd = SAMPLE_SIZE - 1
    sample = buf if len(buf) < SAMPLE_SIZE else buf[0:smpEnd]
    try:
        m.update(sample.encode('utf-8'))
    except:
         clean = sample.decode('iso-8859-1')
         m.update(clean.encode('utf-8'))

    return m.hexdigest()


def inject_file(dbc, fname):

    ourhost = os.getenv("mt_host", socket.gethostname())
    ds = datetime.now().strftime("%F")

    if os.path.isfile(fname):
        fp = open(fname, 'rb')
        buf = fp.read()
        try:
            text = buf.decode('utf-8')
        except UnicodeDecodeError as e:
            text = buf.decode('iso-8859-1').encode('utf8') 
        ids = sample_buffer(text)
        cur = dbc.cursor()
        cur.execute(ijqs, (ids, ds, ourhost, text))

    else:

        raise IOError("Not a regular file")


def inject_dir(dbc, mydir):

    os.chdir(mydir)
    dl = os.listdir()

    for f in dl:
        print("Injecting", f)

        try:
            inject_file(dbc, f)
        except IOError as e:
            print("An Error occured while uploading %s\n", f)
            continue


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("usage: %s <dbname> <file|dir>" % (sys.argv[0]))
        sys.exit(1)
    con = connect_or_create(sys.argv[1])
    if os.path.isdir(sys.argv[2]):
        inject_dir(con, sys.argv[2])
        con.commit()
        con.close()
    elif os.path.isfile(sys.argv[2]):
        inject_file(con, sys.argv[2])
        con.commit()
        con.close()
    else:
        print("Filesystem Error: Unknown inode type\n")
        exit(1)

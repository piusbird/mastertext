#!/usr/bin/env python3

# build the inital blurb table this will be 
# done as a simple script at first I'll make it into 
# a pretty api at some point in the future 
# This is what you might call a 4am prototype
import sys
import sqlite3
from mastertext.common import *
insblrbq ="INSERT INTO blurbs VALUES(?,?)"
sltxtidq = "SELECT rowid,data from hive limit ? offset ?"
LIMIT = 100
offset = 0
BLURBSIZE = 280
if len(sys.argv) < 2:
    print("Give me a database")
    sys.exit(1)

dbq = strict_connect(sys.argv[1])

c = dbq.cursor()
c.execute("SELECT COUNT(*) FROM hive;")
total = c.fetchone()[0] 

while (offset + LIMIT) <= total:
    if ( total - (offset + LIMIT) < LIMIT):
        LIMIT += total - (offset + LIMIT
         
    c.execute(sltxtidq, (LIMIT,offset))
    for r in c.fetchall():
        pid = r[0]
        blurb = r[1][0:BLURBSIZE-1]
        newrow = (pid, blurb)
        c.execute(insblrbq, newrow)

    print("Inserted ", offset, " to ", offset+LIMIT)
    dbq.commit()
    offset += LIMIT


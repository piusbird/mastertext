# Common stuff for mastertext and it's the
# applets use it

import sqlite3
from os.path import exists

dbschema = """
CREATE VIRTUAL TABLE hive USING fts5(id, inject_date, orighost, data);

CREATE TABLE blurbs (
parent_id INTEGER,
blurb VARCHAR(280),
FOREIGN KEY(parent_id) REFERENCES hive(rowid)
);

"""


class MasterTextError(Exception):
    pass


def create_db(fpath):

    if exists(fpath):
        raise MasterTextError("file exists")

    dbcon = sqlite3.connect(fpath)
    cur = dbcon.cursor()
    cur.execute(dbschema)
    dbcon.commit()
    dbcon.close()


def create_or_connect(fpath):

    try:
        create_db(fpath)

    except MasterTextError as e:
        pass
    return sqlite3.connect(fpath)


def strict_connect(fpath):

    if exists(fpath):
        return sqlite3.connect(fpath)
    else:
        raise MasterTextError("db does not exist, strict mode")


connect_or_create = create_or_connect

"""Settings for mastertext"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Flask config object"""

    dbpath = os.getenv("MTDB_PATH") or os.path.abspath("./master.db")
    SECRET_KEY = os.getenv("SECRET_KEY") or "changethisplease"
    DATABASE = {"name": dbpath, "engine": "playhouse.sqlite_ext.SqliteExtDatabase"}
    SECURITY_PASSWORD_SALT = os.getenv("PASSWORD_SALT") or SECRET_KEY
    SECURITY_PRIVATE_INSTANCE = os.getenv("PRIVATE") or True


# FIXME: Find all instances of the old style config and change them
# Get rid of this backward compat symbol afterward
dbpath = Config.dbpath

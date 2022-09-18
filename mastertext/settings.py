# Settings for mastertext
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    dbpath = os.getenv("MTDB_PATH") or './master.db'
    SECRET_KEY = os.getenv("SECRET_KEY") or 'changethisplease'

## FIXME: Find all instances of the old style config and change them
## Get rid of this backward compat symbol afterward
dbpath = Config.dbpath


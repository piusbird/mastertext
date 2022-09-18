from peewee import Model, BareField
from peewee import CharField, IntegerField, DateTimeField, TextField
from peewee import BooleanField
from peewee import ForeignKeyField, CompositeKey
from playhouse.sqlite_ext import SqliteExtDatabase
from playhouse.sqlite_ext import RowIDField, SearchField
from playhouse.sqlite_ext import BlobField, FTS5Model
from mastertext.settings import dbpath
from flask_security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin

database = SqliteExtDatabase(dbpath)  # set database at run time


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Hive(FTS5Model):
    rowid = RowIDField()
    data = SearchField()
    hashid = SearchField()
    inject_date = SearchField()
    orighost = SearchField()

    class Meta:
        table_name = 'hive'
        primary_key = False
        database = database


class Extracts(BaseModel):
    blurb = CharField(null=True)
    parent = ForeignKeyField(column_name='parent_id', model=Hive, null=True)

    class Meta:
        table_name = 'extracts'
        primary_key = False


class HiveConfig(BaseModel):
    k = BareField(primary_key=True)
    v = BareField(null=True)

    class Meta:
        table_name = 'hive_config'


class HiveContent(BaseModel):
    c0 = BareField(null=True)
    c1 = BareField(null=True)
    c2 = BareField(null=True)
    c3 = BareField(null=True)

    class Meta:
        table_name = 'hive_content'


class HiveData(BaseModel):
    block = BlobField(null=True)

    class Meta:
        table_name = 'hive_data'


class HiveDocsize(BaseModel):
    sz = BlobField(null=True)

    class Meta:
        table_name = 'hive_docsize'


class HiveIdx(BaseModel):
    pgno = BareField(null=True)
    segid = BareField()
    term = BareField()

    class Meta:
        table_name = 'hive_idx'
        primary_key = CompositeKey('segid', 'term')


class Link(BaseModel):
    phash = CharField(max_length=40, unique=True, primary_key=True)
    count = IntegerField(null=False, default=0)


class Bookmark(BaseModel):
    phash = CharField(max_length=40, unique=False)
    name = CharField(max_length=250, unique=True, primary_key=True)


class Annotation(BaseModel):
    notehash = CharField(max_length=40, unique=False)
    phash = CharField(max_length=40, unique=False)
    npos = IntegerField(null=False)

class Role(BaseModel, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

class User(BaseModel, UserMixin):
    email = TextField()
    password = TextField()
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)
    fs_uniquifier = CharField(max_length=64, null=False)


class UserRoles(BaseModel):
    # Because peewee does not come with built-in many-to-many
    # relationships, we need this intermediary class to link
    # user to roles.
    user = ForeignKeyField(User, related_name='roles')
    role = ForeignKeyField(Role, related_name='users')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)
# MasterText db functions
from peewee import *
from mastertext.models import *
from mastertext.utils import *
"""
This function fixes a databse corruption issue
that happens in a couple of different ways
Upgrading from v0 to v1 schemea
certian bulk inserts,and there may be others

This results in all or nearly all of the rows in 
the db having the same object id or all of the newly 
inserted rows in the case of bulk inserts

Remember that two or more objects may have the same id on inital insert
because the inital corpus may contain duplicate texts. This is of interst to 
for statistical purposes.

However it is a corruption[1] for most of the data to have the same id value.
This breaks the key bit of the key/value store. I could use a proper k/v store to store 
the data, but that would mean i would have to parially reimplement a whole bunch of
full text search algorithms, and make dup detection almost impossible

footnote 1:Unless you have a database full of 21,000 copies the same Pineapple upside down cake recipe
and in that case You do you, you do you.

You can tell if this has happened if selects on object ids start returning way more rows then is sane
"""
def reid_all_objects(bad_id):

	allData = Hive.select().where(Hive.hashid == bad_id)
	for row in allData.iterator():
		try:
			newid = sha1_id_object(row.data)
		except EncodingError:
			if fix_encoding(row.rowid):
				newid = sha1_id_object(row.data.decode('utf-8'))
			else:
				print("unrecoverable encoding error on " + str(row.rowid))
				break
		roid = row.rowid # I have no control over this confusing variable naming see SQLite docs on rowid
		# basiclly it's the INT PRIMARY KEY implicit by default in all sqlite tables
		# We can't enforce any constraints on an fts5 virtual table
		# hence the sha1 hash ids which are reasonably unique, but as those are unreliable at this point
		# we have to grab the data one row at a time get the hidden rowid feild and use that in our update statement
		print( "Keying " +  str(row.rowid)  + " with " + str(newid) )
		u = Hive.update(hashid=newid).where(Hive.rowid == roid)
		if u.execute() != 1:
			raise MasterTextError("Write my TestCase and replace this error when your done kthanks!")

def fix_encoding(bad_rowid):
	
	qs = Hive.select().where(Hive.rowid == bad_rowid)
	fix = qs[0].data.decode('utf-8')
	u = Hive.update(data=fix).where(Hive.rowid == bad_rowid)
	return u.execute()







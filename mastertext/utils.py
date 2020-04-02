# Utility Functions for mastertext


import hashlib

class MasterTextError(Exception):
    pass

class EncodingError(MasterTextError):
	pass
"""
id_object:
Returns a string containing the 40char object identifier
mastertext is at bottom a fancy key/value store 
with each key being unique. To Ensure this
we generate the unique key of ever text in the db
this is done by hashing every text inserted prepended with a header 
through sha-1.

The header consists of the charecter encoding of the text followed by an ascii space
followed by the text's size in bytes followed by a unicode null byte.
this may remind you of the git object id algorithim. This is not unintentional
""" 
def sha1_id_object(txt, enc='utf-8'):

	
	hdr = enc + ' ' + str(len(txt)) + '\x00'
	try:
		base = hdr + txt
	except TypeError:
		raise EncodingError("not utf-8")
	return hashlib.sha1(base.encode()).hexdigest()



def list_from_file(fname):

	fp = open(fname)
	temp = fp.readlines()
	rt = [l.strip() for l in temp]
	return rt

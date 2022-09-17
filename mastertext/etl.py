"""
MasterText Extract, Transform, Load APIs, 
and related utility functions 
"""
import os
from mastertext.objectstore import TextObjectStore

ts = TextObjectStore()


def inject_file(fname, **kwargs):

    if os.path.isfile(fname) or (os.path.islink(fname) and os.path.isfile(os.readlink(fname))):
        print(fname)
        fp = open(fname, 'rb')
        buffer = fp.read()

        try:
            txt = buffer.decode('utf-8')
        except UnicodeDecodeError:
            txt = buffer.decode('iso-8859-1').encode('utf8')
        return ts.create_object(txt, kwargs)
        if 'destroy' in kwargs:
            if kwargs['destroy']:
                os.unlink(fname)
    else:
        raise IOError("Not A regular file: " + fname)


def crawl_dir(mydir, dest):

    top = os.getcwd()
    subs = []
    if os.path.isdir(mydir):
        os.chdir(mydir)
        contents = os.listdir()
        for f in contents:
            try:
                print(inject_file(f, destroy=dest))
            except IOError as e:
                if os.path.isdir(f):
                    subs.append(f)
                else:
                    raise e

        for s in subs:
            crawl_dir(s)
        os.chdir(top)

    else:
        raise IOError("Not A directory")

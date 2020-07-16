#!/usr/bin/env python3
import sys 
from mastertext.objectstore import TextObjectStore
from mastertext.etl import inject_file, crawl_dir


ts = TextObjectStore()

class MTCommandParser:

    def help(self, args):
        """
        help <subcommandd>
        Display the help text for a subcommand
        """
        subc = getattr(self, args[1], None)
        if subc is not None:
            print(subc.__doc__)
        else:
            print("Command not found")
    
    def get(self, args):
        """
        get <hashid>
        Retrive an object from the store
        """
        if args[1]:
           obj = ts.retrieve_object(args[1])
           print(obj)
        else:
            print(self.help(['get']))


if __name__ == '__main__':

    parser = MTCommandParser()
    cmd = getattr(parser, sys.argv[1], None)
    if cmd is not None:
        cmd(sys.argv[1:])


        
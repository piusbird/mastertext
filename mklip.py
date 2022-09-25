#!/usr/bin/env python3
# Mastertext Cliboard manager
from dbus.mainloop.glib import DBusGMainLoop
import dbus.service
import dbus
from gi.repository import Gtk, Gdk
from mastertext.utils import sha1_id_object
from mastertext.objectstore import *
import re
import fileinput
import signal
import sys
import os
import gi
gi.require_version('Gtk', '3.0')

END_OF_STACK = 'deadbeef' * 5


class NullDevice:
    def write(self, s):
        pass


def hup_handle(sig, fr):
    sys.exit()


class MiniKlipper(dbus.service.Object):
    def __init__(self):
        bus_name = dbus.service.BusName(
            'org.marnold.mklip', bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, '/org/marnold/mklip')
        self.boardxs = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.amal_buffer = None
        self.textstore = TextObjectStore()
        self.hashstack = []
        self.hashstack.append(END_OF_STACK)
        self.forwardstack = []
        self.forwardstack.append(END_OF_STACK)

    @dbus.service.method('org.marnold.mklip')
    def getClipboardContents(self):

        text = self.boardxs.wait_for_text()
        if text == None:
            return "Nothing to read"
        thishash = sha1_id_object(text)
        if thishash != self.hashstack[-1]:
            self.textstore.create_object(text)
            self.hashstack.append(thishash)
        return text

    @dbus.service.method('org.marnold.mklip')
    def getPid(self):

        pidstr = str(os.getpid())
        return pidstr

    @dbus.service.method("org.marnold.mklip")
    def getAmalgamatedBuffer(self):
        if self.amal_buffer is None:
            self.amal_buffer = self.getClipboardContents()

        return self.amal_buffer

    @dbus.service.method("org.marnold.mklip")
    def clearAmalgamatedBuffer(self):
        self.amal_buffer = None

    @dbus.service.method("org.marnold.mklip")
    def toAmalgmatedBuffer(self, text):
        if self.amal_buffer is None:
            self.amal_buffer = text
        else:
            self.amal_buffer += text

    @dbus.service.method("org.marnold.mklip")
    def amalgmateClipboard(self):
        self.toAmalgmatedBuffer(self.getClipboardContents())

    @dbus.service.method("org.marnold.mklip")
    def goBack(self):
        if self.hashstack[-1] == END_OF_STACK:
            return "at last item"
        else:
            ourhash = self.hashstack[-1]
            self.forwardstack.append(self.hashstack.pop())
            return self.textstore.retrieve_object(ourhash)

    @dbus.service.method("org.marnold.mklip")
    def goForward(self):
        if self.forwardstack[-1] == END_OF_STACK:
            return "at first item"
        else:
            ourhash = self.forwardstack[-1]
            self.hashstack.append(self.forwardstack.pop())
            return self.textstore.retrieve_object(ourhash)

    @dbus.service.method("org.marnold.mklip")
    def getHashid(self, hashid):
        if valid_hash(hashid):
            try:
                s = self.textstore.retrieve_object(hashid)
                return s
            except ObjectNotFoundError as e:
                return hashid + " not found"
        else:
            return "Not a valid hash"

    @dbus.service.method("org.marnold.mklip")
    def hiveSearch(self, term):
        result = self.textstore.search_text(term)
        if result['count'] < 1:
            return "0 results for " + term
        else:
            nwstack = reversed(result['ids'])
            self.hashstack.extend(nwstack)
            return str(result['count']) + " documents on the stack"


pid = os.fork()

if pid:
    os._exit(0)  # kill the parent
else:
    # Sets the child process as the pgroup leader
    # which we need to do or we will get killed off
    # when our parent process exits

    os.setpgrp()
    os.umask(0)  # set minimal permissions on all files created from here on

    print(os.getpid())  # to aid in stoping the server
    # Finally we close our connection to the controlling terminal
    # Since in python that's difficult to do without issues
    # we change stdout and stderr to a Null file like object
    sys.stdin.close()
    sys.stdout = NullDevice()
    sys.stderr = NullDevice()

signal.signal(signal.SIGHUP, hup_handle)
signal.signal(signal.SIGTERM, hup_handle)
DBusGMainLoop(set_as_default=True)
myservice = MiniKlipper()
Gtk.main()

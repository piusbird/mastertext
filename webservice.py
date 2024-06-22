#!/usr/bin/env python
from mastertext.objectstore import TextObjectStore, valid_hash, ObjectNotFoundError
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from bottle import Bottle, run, response

app = Bottle()
tso = TextObjectStore()


@app.route("/current")
def current():
    response.set_header("Content-Type", "text/plain")
    bxs = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    text = bxs.wait_for_text()
    tso.create_object(text)
    return text


@app.route("/h/<id>")
def get_byid(id):
    response.set_header("Content-Type", "text/plain")
    if valid_hash(id):
        try:
            s = tso.retrieve_object(id)
            return s
        except ObjectNotFoundError:
            return 404

    return 420


if __name__ == "__main__":
    run(app, host="localhost", port=4241)

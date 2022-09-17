from mastertext.webfrontend import app
from flask import render_template
from mastertext.objectstore import TextObjectStore, valid_hash, ObjectNotFoundError
from mastertext.webfrontend import queries
ts = TextObjectStore()


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Piusbird'}
    latest = queries.get_latest(10)
    return render_template('index.html', title='Home', user=user, newstuff=latest)


@app.route('/d/<string:hashid>')
def view_document(hashid):
    result = ''
    if not valid_hash(hashid):
        return "Not a valid hash", 401

    try:
        result = ts.retrieve_object(hashid)
        data = {'hash': hashid, 'doc': result}
        return render_template('document.html', title="document " + hashid, docdata=data)
    except ObjectNotFoundError as e:
        return str(e), 404


@app.route('/tests/search')
def search_test():
    meta = {"query": "Harry Potter"}
    q = queries.fulltext_search("Harry Potter", 1)
    meta['count'] = q[0]["total"]
    return render_template('results.html',
                           title="Search Results for: " + meta["query"], srs=q, metadata=meta)

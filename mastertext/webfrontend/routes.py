from mastertext.webfrontend import app
from flask import render_template
from mastertext.objectstore import TextObjectStore, valid_hash, ObjectNotFoundError
ts = TextObjectStore()
@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Piusbird'}
    return render_template('index.html', title='Home', user=user)

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




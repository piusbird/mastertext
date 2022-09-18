from mastertext.webfrontend import app
from flask import render_template, request, flash, redirect
from mastertext.objectstore import TextObjectStore, valid_hash, ObjectNotFoundError
from mastertext.webfrontend import queries
from mastertext.webfrontend import forms
from flask_security import Security, PeeweeUserDatastore, \
    UserMixin, RoleMixin, login_required

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
@app.route('/s')
def search_result():
    form = forms.SearchForm(request.args)
    term = request.args.get('term', None)
    if not form.validate() and term is None:
        return render_template('search-main.html', form=form, title="Search")
    
    page = int(request.args.get('page', 1))
    meta = {"query": term}
    meta['page'] = page
    q = queries.fulltext_search(term, page)
    meta['numpages'] = queries.total_pages(term)
    try:
        meta['count'] = q[0]["total"]
    except IndexError as e:
        return "No Such Page", 404
    return render_template('results.html',
                           title="Search Results for: " + meta["query"], srs=q, metadata=meta)

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    form = forms.LoginForm()
#    if form.validate_on_submit():
#        flash('Login requested for user {}, remember_me={}'.format(
#            form.username.data, form.remember_me.data))
#        return redirect('/index')
#    return render_template('login.html', title='Sign In', form=form)


@app.route('/timeline')
@login_required
def timeline():
    timeline = queries.get_latest(250)
    return render_template('timeline.html', title='Global Timeline', newstuff=timeline)
"""Standard routes module"""
from werkzeug.urls import url_parse
import gevent
from peewee import OperationalError
from flask import render_template, request, flash, redirect
from flask import render_template_string
from flask import url_for, Response
from flask_login import login_required
from flask_login import logout_user, login_user
from mastertext.webfrontend import app
from mastertext.webfrontend import queries
from mastertext.webfrontend import forms
from mastertext.singleton import StoreConnect
from mastertext.objectstore import valid_hash
from mastertext.webfrontend.tasks import import_task
from mastertext.objectstore import ObjectNotFoundError
from mastertext.models import NewUser
from mastertext.models import Error



ts = StoreConnect().get_objstore()
bc = app.cache


def flash_back_msgs():
    q = Error.select()
    results = list(q)
    for r in results:
        flash(r.message)
        Error.delete().where(id == r.id) # noqa


@app.route('/')
@app.route('/index')
@login_required
def index():
    flash_back_msgs()
    quicksearch = forms.SearchForm()
    latest = queries.get_latest(10)
    return render_template('index.html', title='Home', newstuff=latest, qs=quicksearch)


@app.route('/d/<string:hashid>')
@login_required
def view_document(hashid):
    flash_back_msgs()
    result = ''
    if not valid_hash(hashid):
        return "Not a valid hash", 401

    if str(hashid) in bc.cache:
        return bc.cache[hashid]
    try:
        result = ts.retrieve_object(hashid)
        data = {'hash': hashid, 'doc': result}
        resp = render_template(
            'document.html', title="document " + hashid, docdata=data)
        bc.cache[hashid] = resp
        return resp
    except ObjectNotFoundError as e:
        return str(e), 404


@app.route('/d/<string:hashid>/orig')
@login_required
def orig_document(hashid):
    result = ''
    if not valid_hash(hashid):
        return "Not a valid hash", 401

    try:
        result = ts.retrieve_object(hashid)
        data = Response(result, mimetype='text/plain')
        return data
    except ObjectNotFoundError as e:
        return str(e), 404


@app.route('/tests/search')
@app.route('/s')
@login_required
def search_result():
    flash_back_msgs()
    form = forms.SearchForm(request.args)
    term = request.args.get('term', None)
    if not form.validate_on_submit() and term is None:
        return render_template('search-main.html', form=form, title="Search")

    page = int(request.args.get('page', 1))
    meta = {"query": term}
    meta['page'] = page
    try:
        q = queries.fulltext_search(term, page)
        meta['numpages'] = queries.total_pages(term)
    except OperationalError as e:
        flash(str(e))
        flash("Try Again!")
        return render_template('search-main.html', title='Search', form=form)
    try:
        meta['count'] = q[0]["total"]
    except IndexError as e:
        return "No Such Page " + str(e), 404
    return render_template('results.html',
                           title="Search Results for: " + meta["query"], srs=q, metadata=meta)


@app.route('/tests/home')
@login_required
def home():
    return render_template_string("Hello {{ current_user.username }}")


@login_required
@app.route('/timeline')
def timeline():
    flash_back_msgs()
    tl = queries.get_latest(250)
    return render_template('timeline.html', title='Global Timeline', newstuff=tl)


@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_blob():
    flash_back_msgs()
    form = forms.CreateForm()
    clone = request.args.get('clone', None)
    title = "Create a Blob"
    if form.validate_on_submit():
        blobinfo = ts.create_object(form.body.data)
        if blobinfo['count'] == 1:
            flash(blobinfo['hash'] + " Created Successfully")
            nwloc = blobinfo['hash']
            return redirect(f'/d/{nwloc}')
        if blobinfo['count'] > 1:
            nwloc = blobinfo['hash']
            return redirect(f'/d/{nwloc}')

    if clone is not None:
        form.body.data = ts.retrieve_object(clone)
        title = "Clone " + clone
    return render_template('create.html', title=title, form=form)


@app.route('/import', methods=['GET', 'POST'])
@login_required
def data_import():
    flash_back_msgs()
    form = forms.ImportForm()
    if form.validate_on_submit():
        target = form.import_url.data
        gevent.spawn(import_task, target)
        flash(f'{target} Importing')
        return redirect(url_for('data_import'))
    # general case
    return render_template('data-import.html', form=form, title="Data Import")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():  # noqa
        user = NewUser.get(NewUser.username == form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    else: # noqa
        return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    flash("Goodbye!")
    logout_user()
    return redirect(url_for('index'))

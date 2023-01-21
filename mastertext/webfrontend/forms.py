"""WTForms classes for webfrontend"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, URL
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SearchForm(FlaskForm):
    """Search form"""

    term = StringField("Search Query", validators=[DataRequired()])
    submit = SubmitField("Go!")


class CreateForm(FlaskForm):
    """Blob Creation form"""

    body = StringField("Create A Blob", widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("New")


class ImportForm(FlaskForm):
    """Data importer form"""

    import_url = StringField("Webpage to Import", validators=[DataRequired(), URL()])
    submit = SubmitField("Go!")

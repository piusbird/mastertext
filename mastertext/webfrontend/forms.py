from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SearchForm(FlaskForm):
    term = StringField('Search Query', validators=[DataRequired()])
    submit = SubmitField('Go!')

class CreateForm(FlaskForm):
    body = StringField(u'Create A Blob', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField("New")

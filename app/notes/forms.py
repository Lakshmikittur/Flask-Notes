from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
import app.accounts._common as  accounts_common_helpers


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=20, min=1, message="Title must be between 1 and 20 characters")])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
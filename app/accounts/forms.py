from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app.accounts.models import User
import app.accounts._common as  accounts_common_helpers


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    fullname = StringField('Fullname', validators=[DataRequired(), Length(min=2, max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=6, max=30)])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        #if current_user.username != username.data:
        user = accounts_common_helpers.get_user_from_username(username.data)
        if user:
            raise ValidationError("Username exits! Choose another username")

    def validate_email(self,email):
        #if current_user.email != email.data:
        user = accounts_common_helpers.get_user_from_emailID(email.data)
        if user:
            raise ValidationError("Email exits! Choose another Email")



class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email(), Length(min=2, max=30)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


# class UpdateForm(FlaskForm):
#     username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
#     email = StringField('Email', validators=[DataRequired(), Email()])
#     picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
#     submit = SubmitField('Update')

#     def validate_username(self,username):
#         if username.data != current_user.username:
#             user = User.query.filter_by(username = username.data).first()
#             if user:
#                 raise ValidationError("Username exits! Choose another username")

#     def validate_email(self,email):
#         if email.data != current_user.email:
#             user = User.query.filter_by(email = email.data).first()
#             if user:
#                 raise ValidationError("Email exits! Choose another Email")
# class RequestResetForm(FlaskForm):
#     email=StringField('Email',
#                         validators=[DataRequired(), Email()])
#     submit = SubmitField('Request Password Reset')

#     def validate_email(self,email):
#         #if current_user.email != email.data:
#         user = User.query.filter_by(email = email.data).first()
#         if user is None:
#             raise ValidationError("There is no account with that email. you must register first")

# class ResetPasswordForm(FlaskForm):
#     password = PasswordField('Password', validators=[DataRequired()])
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Request Password')

from app import db, login_manager
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable = False, unique = True)
    fullname = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(256), nullable = False)
    emailID = db.Column(db.String(40), nullable = False, unique = True)
    notes = db.relationship('Note', backref = "author", lazy = True )


    def __init__(self, username, fullname, password, emailID):
        self.username = username
        self.fullname = fullname
        self.password = password
        self.emailID = emailID

    def __repr__(self):
        return f"Username: {self.username}, Full Name: {self.fullname}, Email: {self.emailID}"

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'emailID': self.emailID,
            'password': self.password,
            'fullname': self.fullname
        }


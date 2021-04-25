# This file contains the common functions that Accounts API and Web routes can share
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.accounts.models import User

PASSWORD_SALT_LENGTH = 8

def get_user_from_ID(ID):
    tempUser = User.query.filter_by(id=ID).first()
    if tempUser is None:
        return False
    else:
        return tempUser

def get_user_from_username(username):
    tempUser = User.query.filter_by(username=username).first()
    if tempUser is None:
        return False
    else:
        return tempUser

def get_user_from_emailID(emailID):
    tempUser = User.query.filter_by(emailID=emailID).first()
    if tempUser is None:
        return False
    else:
        return tempUser

def check_username_password(username, password):
    tempUser = get_user_from_username(username)
    if tempUser == False or check_password_hash(tempUser.password,password) != True:
        return False
    else:
        return True

def check_emailID_password(emailID, password):
    tempUser = get_user_from_emailID(emailID)
    if tempUser == False or check_password_hash(tempUser.password,password) != True:
        return False
    else:
        return True

def create_user(userObject):
    if get_user_from_username(userObject.username) != False:
        return "Username already exists"
    if get_user_from_emailID(userObject.emailID) != False:
        return "Email ID already exists"
    userObject.password = generate_password_hash(userObject.password,method="pbkdf2:sha256",salt_length=PASSWORD_SALT_LENGTH)
    db.session.add(userObject)
    db.session.commit()
    return True

def update_user_info(userObject):
    tempUser = get_user_from_ID(userObject.ID)
    if tempUser == None:
        return "User not found"
    ConflictingUsers = User.query.filter_by(emailID=userObject.emailID,username=userObject.username).all()
    if len(ConflictingUsers) >= 2:
        return "Conflict detected"
    elif len(ConflictingUsers) == 1 and ConflictingUsers[0].id==tempUser.id:
        tempUser.username = userObject.username
        tempUser.emailID = userObject.emailID
        tempUser.fullname = userObject.fullname
        db.session.commit()
        return True
    else:
        return "Conflict detected"

def update_user_password(username, newPassword):
    tempUser = get_user_from_username(username)
    if tempUser == False:
        return "User not found"
    tempUser.password = generate_password_hash(newPassword,method="pbkdf2:sha256",salt_length=PASSWORD_SALT_LENGTH)
    db.session.commit()
    return True

def delete_user_by_ID(userID):
    tempUser = get_user_from_ID(userID)
    if tempUser == None:
        return "User not found"
    db.session.delete(tempUser)
    db.session.commit()
    return True

def get_all_users_list():
    return User.query.all()
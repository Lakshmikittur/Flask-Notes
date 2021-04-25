from flask import Blueprint, request, url_for, abort
import app.accounts._common as  accounts_common_helpers
from app.accounts.models import User
from app import db
from json import dumps as dmp

accounts_api_router = Blueprint('accounts', __name__, url_prefix = "/api/accounts")

@accounts_api_router.route("/checkusername", methods = ["GET"])
def check_if_username_exists():
    if "username" in request.values:
        if accounts_common_helpers.get_user_from_username(request.values["username"]) == False:
            return dmp(False)
        else:
            return dmp(True)
    return dmp(False)

@accounts_api_router.route("/checkemailid", methods = ["GET"])
def check_if_emailID_exists():
    if "emailID" in request.values:
        if accounts_common_helpers.get_user_from_emailID(request.values["emailID"]) == False:
            return dmp(False)
        else:
            return dmp(True)
    return dmp(False)

@accounts_api_router.route("/checkusernameandpassword", methods = ["POST"])
def check_if_username_password_correct():
    if "username" in request.values and "password" in request.values:
        if accounts_common_helpers.check_username_password(request.values["username"], request.values["password"]) == False:
            return dmp(False)
        else:
            return dmp(True)
    return dmp(False)

@accounts_api_router.route("/checkemailandpassword", methods = ["POST"])
def check_if_email_password_correct():
    if "emailID" in request.values and "password" in request.values:
        if accounts_common_helpers.check_emailID_password(request.values["emailID"], request.values["password"]) == False:
            return dmp(False)
        else:
            return dmp(True)
    return dmp(False)

@accounts_api_router.route('/createuser', methods = ["POST"])
def create_user():
    if "username" in request.values and "fullname" in request.values and "emailID" in request.values and "password" in request.values:
        newUser = User(fullname = request.values["fullname"], emailID = request.values["emailID"], password = request.values["password"], username = request.values["username"])
        result = accounts_common_helpers.create_user(newUser)
        if result == True:
            return dmp(newUser.id)
        else:
            return dmp(result)
    return dmp("Required parameter/s missing")

@accounts_api_router.route("/getuserbyid", methods = ["GET"])
def get_user_by_ID():
    if "id" in request.values:
        tempUser = accounts_common_helpers.get_user_from_ID(request.values["id"])
        if tempUser == False:
            return dmp(False)
        else:
            return tempUser.serialize()
    else:
        return dmp(False)

@accounts_api_router.route('/getallusers', methods = ["GET"])
def get_all_users():
    allUsers = accounts_common_helpers.get_all_users_list()
    allUsers = [user.serialize() for user in allUsers]
    return dmp(allUsers)
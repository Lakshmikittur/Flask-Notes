from flask import Blueprint, request, url_for, abort
import app.notes._common as  notes_common_helpers
import app.accounts._common as accounts_common_helpers
from app.notes.models import Note
from app.accounts.models import User
from app import db
from json import dumps as dmp


notes_api_router = Blueprint('notes', __name__, url_prefix = "/api/notes")


@notes_api_router.route('/createnote', methods=["POST"])
def createnote():
    if "username" in request.values and "password" in request.values and "content" in request.values:
        if accounts_common_helpers.check_username_password(request.values["username"], request.values["password"]):
            tempUser = accounts_common_helpers.get_user_from_username(request.values["username"])
            newnote = Note(author_id = tempUser.id, content = request.values["content"])
            result = notes_common_helpers.createnote(newnote)
            if result:
                return dmp(newnote.id)
            else:
                return dmp(result)
        else:
            return dmp("Username/password invalid")
    return dmp("Required parameter/s missing")

@notes_api_router.route('/allnotes', methods=["GET"])
def allnotes():
    notes_list = notes_common_helpers.allnotes()
    notesserialized = [note.serialize() for note in notes_list]
    return dmp(notesserialized)

@notes_api_router.route('/editnote', methods=["POST"])
def editnote():
    if "username" in request.values and "password" in request.values and "noteid" in request.values and "content" in request.values:
        user_valid = accounts_common_helpers.check_username_password(request.values["username"], request.values["password"])
        if user_valid:
            tempUser = accounts_common_helpers.get_user_from_username(request.values["username"])
            if notes_common_helpers.checknoteidbyauthorid(tempUser.id, request.values["noteid"]):
                content = request.values["content"]
                tempnote = notes_common_helpers.editnote( request.values["noteid"], content)            
                return dmp(True)
            else:
                return dmp("You dont have authorisation to edit the note")
        else:
            return dmp("Invalid username/password")

    return dmp("Invalid request paramter/s")

@notes_api_router.route('/deletenote', methods=["POST"])
def deletenote():
    if "username" in request.values and "password" in request.values and "noteid" in request.values:
        user_valid = accounts_common_helpers.check_username_password(request.values["username"], request.values["password"])
        if user_valid:
            tempUser = accounts_common_helpers.get_user_from_username(request.values["username"])
            if notes_common_helpers.checknoteidbyauthorid(tempUser.id, request.values["noteid"]):
                notes_common_helpers.deletenote( request.values["noteid"])            
                return dmp(True)
            else:
                return dmp("You dont have authorisation to delete the note")
        else:
            return dmp("Invalid username/password")

    return dmp("Invalid request paramter/s")


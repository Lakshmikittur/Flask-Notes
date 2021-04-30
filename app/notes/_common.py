from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from app import db
from app.notes.models import Note
import app.accounts._common as accounts_common_helpers
from datetime import datetime

def createnote(noteobj):
    db.session.add(noteobj)
    db.session.commit()
    return True

def allnotes():
    return Note.query.all()

def getnotebyId(id):
    noteobj = Note.query.filter_by(id = id).first()
    if noteobj:
        return noteobj
    else:
        return False

# def checknoteidbyauthorid(author_id, note_id):
#     user = accounts_common_helpers.get_user_from_ID(author_id)
#     for note in user.notes:
#         if note.id == int(note_id):
#             return True    
#     return False

def checknoteidbyauthorid(author_id, note_id):
    note = getnotebyId(note_id)
    if note:
        if note.author_id == int(author_id):
            return True
        else:
            return False
    return False


def editnote(id, content, title):
    noteobj = getnotebyId(id)
    if noteobj:
        noteobj.content = content
        noteobj.title = title
        noteobj.date_modified = datetime.utcnow()
        db.session.commit()
        return True
    
    return False

def deletenote(id):
    noteobj = getnotebyId(id)
    if noteobj:
        db.session.delete(noteobj)
        db.session.commit()
    return True
    
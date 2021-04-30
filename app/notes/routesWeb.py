from flask import url_for, abort, flash, render_template, request, Blueprint, redirect
from flask_login import login_user, current_user, logout_user, login_required
import app.accounts._common as  accounts_common_helpers
import app.notes._common as notes_common_helpers
from app.accounts.models import User
from app.notes.models import Note
from app import db
from json import dumps as dmp
from app.notes.forms import PostForm


notes_web_router = Blueprint('notesweb', __name__, url_prefix = "/notes")

@notes_web_router.route('/newnote',methods=['GET','POST'])
@login_required
def newnote():
    if request.method == 'GET':
        form = PostForm()
        return render_template('notes/newnote.html',form=form, title='newnote')
    else:
        form = PostForm()
        if form.validate_on_submit():
            noteobj = Note(title=form.title.data, content=form.content.data, author_id=current_user.id)
            note_created = notes_common_helpers.createnote(noteobj)
            if note_created:
                flash('New note added succesfully','success')
                return redirect(url_for('notesweb.note', note_id = noteobj.id))
            else:
                flash('Unable to add new note','danger')
        return render_template('notes/newnote.html',form=form, title='newnote')


@notes_web_router.route('/note/<int:note_id>')
@login_required
def note(note_id):    
    if notes_common_helpers.checknoteidbyauthorid(current_user.id, note_id):
        noteobj = notes_common_helpers.getnotebyId(note_id)
        return render_template('notes/note.html', title = noteobj.title, noteobj=noteobj)
    else:
        flash('You cannot access this note')
        abort(403)

@notes_web_router.route('/note/<int:note_id>/edit',methods=["GET","POST"])
@login_required
def editnote(note_id):
    if not notes_common_helpers.checknoteidbyauthorid(current_user.id, note_id):
        abort(403) #http response for forbidden route
    
    form = PostForm()
    #populate for get request
    if request.method == "GET":
        noteobj = notes_common_helpers.getnotebyId(note_id)
        form.title.data = noteobj.title
        form.content.data = noteobj.content
        
    else :
        if form.validate_on_submit():
            editnote = notes_common_helpers.editnote(note_id, form.content.data, form.title.data)
            if editnote == True:
                flash("Your note has been updated",'success')
                x = [print(note.content) for note in current_user.notes]
                return redirect(url_for('notesweb.note', note_id= note_id))   
            else:
                flash("This note does not exist") 

    return render_template('notes/newnote.html',title='Edit Note',
    form=form)


@notes_web_router.route('/note/<int:note_id>/delete', methods=["GET"])
@login_required
def deletenote(note_id):


    if not notes_common_helpers.checknoteidbyauthorid(current_user.id, note_id):
        abort(403) #http response for forbidden route
    
    #form = PostForm()
    #noteobj = notes_common_helpers.getnotebyId(note_id)
    # form.title.data = noteobj.title
    # form.content.data = noteobj.content
    
    notes_common_helpers.deletenote(note_id)
    flash("Your Note is Deleted",'success')
    return redirect(url_for('accountsweb.usernotes'))
    








from flask import url_for, abort, flash, render_template, request, Blueprint, redirect
from flask_login import login_user, current_user, logout_user, login_required
import app.accounts._common as  accounts_common_helpers
import app.notes._common as notes_common_helpers
from app.accounts.models import User
from app.notes.models import Note
from app import db
from json import dumps as dmp
from app.accounts.forms import LoginForm, RegistrationForm

accounts_web_router = Blueprint('accountsweb', __name__, url_prefix = "/accounts")

@accounts_web_router.route('/register', methods=['GET','POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('r'))
    if request.method == "GET":
        form = RegistrationForm()
        return render_template('accounts/register.html', title="register", form=form)
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username= form.username.data, fullname= form.fullname.data, emailID=form.email.data, password= form.password.data)
            user_created = accounts_common_helpers.create_user(user)
            if user_created == True:
                flash(f'Your account has been created succesfully. LogIn to post ','success')
                return redirect(url_for('accountsweb.login'))
            else:
                flash(user_created,'danger')
        return render_template('accounts/register.html', title="register", form=form)



@accounts_web_router.route('/login', methods=['GET','POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    if request.method == "GET":
        form = LoginForm()
        return render_template('accounts/login.html', title="login", form=form)
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user_present = accounts_common_helpers.check_emailID_password(form.email.data, form.password.data)
            if user_present == True:
                user = accounts_common_helpers.get_user_from_emailID(form.email.data)
                if user:
                    login_user(user, form.remember.data)
                    flash("Logged In", 'success')
                    return redirect(url_for('accountsweb.register'))
                else:
                    flash('Login Unsuccesful','danger')
            else:
                flash('Please register before loggin in', 'warning')
                return redirect(url_for('accountsweb.login'))
        return render_template('accounts/login.html', title="login", form=form)


@accounts_web_router.route('/usernotes', methods=["GET"])
@login_required
def usernotes():
    user = accounts_common_helpers.get_user_from_username(current_user.username)
    return render_template('notes/user_notes.html', noteobjs = user.notes)

@accounts_web_router.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    flash('You are logged out', 'success')
    return redirect(url_for('accountsweb.login'))





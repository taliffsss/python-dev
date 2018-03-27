from __future__ import print_function
from flask import Flask, render_template, flash, abort, request, url_for, redirect, session, send_from_directory, jsonify, Blueprint
from flask_wtf import FlaskForm
import os
from cms import Content
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField, ValidationError, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
import gc
import datetime
import pytz
from pytz import timezone
from model import check_username, get_id, tracked_loggedin, logout_update, register, unique_username, unique_email, get_role, msgme, webhook, unreadmsg, getUnreadmsg, countVisitors, getVisitors, visitorCountAll, getMessage, updateMessage, getAllMessage
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware
import subprocess
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter

now = datetime.datetime.now()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

y = now.year

TOPIC_DICT = Content()

app = Flask(__name__)
bootstrap = Bootstrap(app)

proxies = ('110.54.244.105','209.146.28.238','203.82.37.6', '208.80.194.29', '208.80.194.30','208.80.194.31', '208.80.194.32','208.80.194.33', '208.80.194.35','121.58.234.74','112.200.108.51','46.243.189.60','27.145.67.10','89.252.163.56','123.141.64.130','114.18.75.220','46.243.189.99','185.232.65.203','212.83.150.74')

fpath = app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
fmax = app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

class Message(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    messageme = TextField('Message', validators=[DataRequired()],widget=TextArea())

@app.route('/',methods=["GET","POST"])
def homepage():
    try:
        form = Message(request.form)
        if request.method == "POST" and form.validate():
            name  = form.name.data
            msg = form.messageme.data
            flash("Your message has been submit")
            msgme(name,msg)
            return redirect(url_for("homepage"))

        webhook()
        return render_template("home.html", TOPIC_DICT = TOPIC_DICT, title="Home", y=y, form=form)
    except Exception as e:
        return(str(e))

@app.before_request
def limit_remote_addr():
    remote = request.remote_addr
    while remote in proxies:
        abort(403)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap

@app.route("/port-logout/")
@login_required
def logout():
    uname = session['username']
    uid = get_id(uname)
    logout_update(uid)
    webhook()
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('login_page'))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(fpath, filename))
            return redirect(url_for('login_page'))
    return ''

class loginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

@app.route('/port-login/', methods=["GET","POST"])
def login_page():
    error = ''
    try:
        form = loginForm(request.form)

        if 'logged_in' in session:
            return redirect(url_for("homepage"))
        else:
            if request.method == "POST" and form.validate():
                uname = form.username.data
                password = form.password.data
                data = check_username(uname)
                if sha256_crypt.verify(password, data):
                    session['logged_in'] = True
                    session['username'] = uname
                    uid = get_id(uname)
                    tracked_loggedin(uid)
                    flash("You are now logged in")
                    return redirect(url_for("dashboard"))

                else:
                    error = "Invalid credentials, try again."

            gc.collect()
            webhook()
            return render_template("login.html", error=error,title="Login",y=y,form=form)

    except Exception as e:
        #flash(e)
        error = "Invalid Username or Password"
        return render_template("login.html", error=error,title="Login",y=y,form=form)

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('New Password', [validators.Length(min=8, max=50),
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    address = StringField('Address', validators=[DataRequired()])

@app.route('/port-dashboard/register/', methods=["GET","POST"])
@login_required
def register_page():
    try:
        form = RegistrationForm(request.form)
        role = get_role()
        if request.method == "POST" and form.validate():
            uname  = form.username.data
            email = form.email.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            role = request.form['role']
            address = form.address.data
            password = sha256_crypt.encrypt((str(form.password.data)))

            x = unique_username(uname)
            e = unique_email(email)

            if int(x) > 0:
                flash("That username is already taken, please choose another")
                return render_template('register.html', form=form,title="Registration Form",role=role)

            else:

                if int(e) > 0:
                    flash("That email is already taken, please choose another")
                    return render_template('register.html', form=form,title="Registration Form",role=role)
                else:
                    register(uname,password,email,firstname,lastname,role,address)
                    
                    flash("Thanks for registering!")

                    return redirect(url_for('login_page'))
        webhook()
        msg = unreadmsg()
        if msg == 0:
            s = ''
        else:
            s = unreadmsg()
        unread = getUnreadmsg()
        visit = countVisitors()
        return render_template("register.html", form=form,title="Registration Form",role=role,unread=unread,visit=visit)

    except Exception as e:
        return(str(e))


@app.route('/port-dashboard/')
@login_required
def dashboard():
    webhook()
    msg = unreadmsg()
    if msg == 0:
        s = ''
    else:
        s = unreadmsg()
    unread = getUnreadmsg()
    visit = countVisitors()
    list = getUnreadmsg()
    msglist = getAllMessage()
    return render_template("admin/dashboard.html",title="Dashboard",s=s,unread=unread,visit=visit,list=list,msglist=msglist)

@app.route('/port-dashboard/message/<int:msgid>')
@login_required
def messages(msgid):
    webhook()
    updateMessage(msgid)
    msg = unreadmsg()
    if msg == 0:
        s = ''
    else:
        s = unreadmsg()
    unread = getUnreadmsg()
    rmsg = getMessage(msgid)
    visit = countVisitors()
    return render_template("admin/message.html",title="Dashboard",s=s,unread=unread,visit=visit,rmsg=rmsg)

@app.route('/port-dashboard/visitor/')
@login_required
def visitor():
    webhook()
    msg = unreadmsg()
    if msg == 0:
        s = ''
    else:
        s = unreadmsg()
    unread = getUnreadmsg()
    visit = countVisitors()
    guest = getVisitors()
    countAll = visitorCountAll()
    return render_template("admin/visitors.html",title="Dashboard",s=s,unread=unread,visit=visit,guest=guest)

@app.errorhandler(404)
def page_not_found(e):
    webhook()
    return render_template("error/page_not_found.html")

if __name__ == "__main__":
    app.run()

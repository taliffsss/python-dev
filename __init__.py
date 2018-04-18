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
from model import check_username, get_id, tracked_loggedin, logout_update, register, unique_username, unique_email, get_role, msgme, webhook, unreadmsg, getUnreadmsg, countVisitors, getVisitors, visitorCountAll, getMessage, updateMessage, getAllMessage, block_ip, check_ip, block_client_ip, block_ip, getIDBlock_ip, updateBlock_ip, getAllBlock_ip, getVisitorsoftheDay, verifyParam, removeIP
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware
import subprocess
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination, get_page_parameter
import pusher

now = datetime.datetime.now()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

y = now.year

#Set TimeZone
os.environ['TZ'] = 'Asia/Manila'

#Current Date
d = now.strftime('%Y-%m-%d')

TOPIC_DICT = Content()

app = Flask(__name__)
bootstrap = Bootstrap(app)

fpath = app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
fmax = app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

pusher_client = pusher.Pusher(
    app_id='509979',
    key='0d3d93458b799c00839c',
    secret='8f112e2f0bd4bc02244f',
    cluster='ap1',
    ssl=True
)
#pusher_client.trigger('my-channel', 'my-event', {'message': 'Python Portfolio'})

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

        if request.remote_addr != '202.151.35.180':
            webhook()
        return render_template("home.html", TOPIC_DICT = TOPIC_DICT, title="Home", y=y, form=form)
    except Exception as e:
        return(str(e))

@app.before_request
def limit_remote_addr():
    remote = request.remote_addr
    ip = block_ip()
    for c in ip:
        bip = c[1]
        if remote == bip:
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

@app.route("/py-logout/")
@login_required
def logout():
    uname = session['username']
    uid = get_id(uname)
    logout_update(uid)
    if request.remote_addr != '202.151.35.180':
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

@app.route('/py-login/', methods=["GET","POST"])
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
            if request.remote_addr != '202.151.35.180':
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

@app.route('/py-dashboard/register/', methods=["GET","POST"])
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

        if request.remote_addr != '202.151.35.180':
            webhook()
        msg = unreadmsg()
        if msg == 0:
            s = ''
        else:
            s = unreadmsg()
        unread = getUnreadmsg()
        visit = countVisitors()
        return render_template("register.html", form=form,title="Registration Form",role=role,unread=unread,visit=visit,d=d)

    except Exception as e:
        return(str(e))

class BlockClientIP(FlaskForm):
    clientip = StringField('Client IP', validators=[DataRequired()])

@app.route('/py-dashboard/')
@login_required
def dashboard():

    if request.remote_addr != '202.151.35.180':
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
    blockip = BlockClientIP(request.form)
    return render_template("admin/dashboard.html",blockip=blockip,title="Dashboard",s=s,unread=unread,visit=visit,msglist=msglist,d=d)

@app.route('/py-dashboard/message/<int:msgid>')
@login_required
def messages(msgid):

    if request.remote_addr != '202.151.35.180':
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
    blockip = BlockClientIP(request.form)
    return render_template("admin/messages.html",blockip=blockip,title="Dashboard",s=s,unread=unread,visit=visit,rmsg=rmsg,d=d)

@app.route('/py-dashboard/visitor/')
@login_required
def visitor():

    if request.remote_addr != '202.151.35.180':
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
    blockip = BlockClientIP(request.form)
    return render_template("admin/visitors.html",blockip=blockip,title="Dashboard",s=s,unread=unread,visit=visit,guest=guest,d=d)

@app.route('/py-dashboard/visitor/<datesNow>')
@login_required
def visitor_now(datesNow):

    try:
        if request.remote_addr != '202.151.35.180':
            webhook()

        c = verifyParam(datesNow)

        if int(c) > 0:
            msg = unreadmsg()
            if msg == 0:
                s = ''
            else:
                s = unreadmsg()
            unread = getUnreadmsg()
            visit = countVisitors()
            guest = getVisitorsoftheDay(datesNow)
            countAll = visitorCountAll()
            blockip = BlockClientIP(request.form)

            return render_template("admin/visitor_of_the_day.html",blockip=blockip,title="Dashboard",s=s,unread=unread,visit=visit,guest=guest,d=d)

        else:

            return render_template("error/page_not_found.html",title="Page Not Found")

    except Exception as e:
        return(str(e))

@app.route('/py-dashboard/block-ip/', methods=["GET","POST"])
@login_required
def client_ip():
    try:
        msg = unreadmsg()
        if msg == 0:
            s = ''
        else:
            s = unreadmsg()
        unread = getUnreadmsg()
        visit = countVisitors()
        msglist = getAllMessage()
        if request.remote_addr != '202.151.35.180':
            webhook()
        blockip = BlockClientIP(request.form)

        if request.method == "POST" and blockip.validate():

            clientip  = blockip.clientip.data

            x = check_ip(clientip)

            if int(x) > 0:
                flash("That IP is already exist")
                return render_template('admin/dashboard.html',blockip=blockip,title="Dashboard",s=s,unread=unread,visit=visit,msglist=msglist,d=d)

            else:
                block_client_ip(clientip)

                flash("Successfully added")

                return redirect(url_for('dashboard'))

        return render_template("admin/dashboard.html",blockip=blockip,title="Dashboard",s=s,unread=unread,visit=visit,msglist=msglist,d=d)

    except Exception as e:
        return(str(e))

@app.route('/py-dashboard/block-ip-list/')
@login_required
def block_list():

    if request.remote_addr != '202.151.35.180':
        webhook()
    msg = unreadmsg()
    if msg == 0:
        s = ''
    else:
        s = unreadmsg()
    unread = getUnreadmsg()
    visit = countVisitors()
    msglist = getAllMessage()
    blockip = BlockClientIP(request.form)
    blocklist = getAllBlock_ip()
    return render_template("admin/block-list.html",blockip=blockip,title="Dashboard",s=s,unread=unread,visit=visit,msglist=msglist,blocklist=blocklist,d=d)

@app.route('/py-dashboard/block-ip-list/unblock/<int:blockid>', methods=["GET","POST"])
@login_required
def unblock_client_ip(blockid):
    try:
        c = getIDBlock_ip(blockid)
        cbid = 0
        if int(c) > 0:
            updateBlock_ip(blockid,cbid)
            flash("Successfully Update")
            return redirect(url_for('block_list'))
        else:
            flash("Invalid ID")
            return redirect(url_for('block_list'))

    except Exception as e:
        return(str(e))

@app.route('/py-dashboard/block-ip-list/block/<int:blockid>', methods=["GET","POST"])
@login_required
def blockClient_ip(blockid):
    try:
        c = getIDBlock_ip(blockid)
        cbid = 1
        if int(c) > 0:
            updateBlock_ip(blockid,cbid)
            flash("Successfully Update")
            return redirect(url_for('block_list'))
        else:
            flash("Invalid ID")
            return redirect(url_for('block_list'))

    except Exception as e:
        return(str(e))

@app.route('/py-dashboard/block-ip-list/remove/<int:blockid>', methods=["GET","POST"])
@login_required
def reoveBlockIP(blockid):
    try:
        c = getIDBlock_ip(blockid)

        if int(c) > 0:
            removeIP(blockid)
            flash("Data has been Deleted")
            return redirect(url_for('block_list'))
        else:
            flash("Invalid ID")
            return redirect(url_for('block_list'))

    except Exception as e:
        return(str(e))

@app.errorhandler(404)
def page_not_found(e):
    if request.remote_addr != '202.151.35.180':
        webhook()
    return render_template("error/page_not_found.html",title="Page Not Found")

if __name__ == "__main__":
    app.run()

from __future__ import print_function
from flask import Flask, render_template, flash, request, url_for, redirect, session, send_from_directory
from flask_wtf import FlaskForm
import os
from cms import Content
from conn import connection
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField, ValidationError, SelectField
from wtforms.validators import DataRequired
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart
from functools import wraps
import gc
from selenium import webdriver
import datetime
import pytz
from pytz import timezone
from model import check_username, get_id, tracked_loggedin, logout_update, register, unique_username, unique_email, get_role
from werkzeug.utils import secure_filename
from werkzeug import SharedDataMiddleware
import subprocess
from flask_mail import Mail
from flask_bootstrap import Bootstrap

# MAIL_SERVER=smtp.googlemail.com
# MAIL_PORT=587
# MAIL_USE_TLS=1
# MAIL_USERNAME=<your-gmail-username>
# MAIL_PASSWORD=<your-gmail-password>

now = datetime.datetime.now()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

y = now.year

TOPIC_DICT = Content()

app = Flask(__name__)
bootstrap = Bootstrap(app)

#mail = Mail(app)

fpath = app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
fmax = app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def homepage():
	return render_template("home.html", TOPIC_DICT = TOPIC_DICT, title="Home", y=y)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap

@app.route("/logout/")
@login_required
def logout():
    uname = session['username']
    uid = get_id(uname)
    logout_update(uid)
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

@app.route('/login/', methods=["GET","POST"])
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

            return render_template("login.html", error=error,title="Login",y=y,form=form)

    except Exception as e:
        #flash(e)
        error = "Invalid Username or Password"
        return render_template("login.html", error=error,title="Login",y=y,form=form)

class RegistrationForm(FlaskForm):
    role = get_role()
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

@app.route('/register/', methods=["GET","POST"])
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

        return render_template("register.html", form=form,title="Registration Form",role=role)

    except Exception as e:
        return(str(e))


@app.route('/dashboard/')
@login_required
def dashboard():
    return render_template("admin/dashboard.html",title="Dashboard")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/page_not_found.html")

if __name__ == "__main__":
    app.secret_key = '$5$rounds=535000$LjDiH2YmB1rSkSNi$0ZJznZe32eIAcvHvrh5/vIEmWWXTs8SPND7oFypdog6'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.debug = True
    app.run()
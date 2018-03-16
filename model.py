from conn import connection
import time
import datetime
import pytz
from pytz import timezone
from MySQLdb import escape_string as thwart

#Set TimeZone
asia = timezone('Asia/Manila')

#Current Date Time
now = datetime.datetime.now()

timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

#Get ID
def get_id(uname):
	c, conn = connection()
	date = c.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

	data = c.fetchone()[0]

	return data

#Check Username
def check_username(uname):
	c, conn = connection()
	date = c.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

	data = c.fetchone()[2]

	return data

#Check if Usernamme is available
def unique_username(uname):
	c, conn = connection()
	data = c.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

	return data

#Check if Usernamme is available
def unique_email(email):
	c, conn = connection()
	data = c.execute("SELECT * FROM users WHERE email = (%s)",(email,))

	return data

#Log User Loggedin
def tracked_loggedin(uid):
	c, conn = connection()
	data = c.execute("INSERT INTO py_loggedin_activity (userid, loggedin) VALUES (%s, %s)",(uid,timestamp))

	conn.commit()

#Update Logout
def logout_update(uid):
	c, conn = connection()
	data = c.execute("UPDATE py_loggedin_activity SET loggedout = %s WHERE userid = %s AND loggedout IS NULL",(timestamp,uid))

	conn.commit()

def register(uname,password,email,firstname,lastname):
	c, conn = connection()
	c.execute("INSERT INTO users (username, password, email, firstname, lastname, date_created) VALUES (%s, %s, %s, %s, %s, %s)",(thwart(uname), thwart(password), thwart(email), thwart(firstname), thwart(lastname), timestamp))

	conn.commit()
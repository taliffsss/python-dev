from conn import connection, failover
import os
import time
import datetime
import pytz
from pytz import timezone
from MySQLdb import escape_string as thwart
from flask import request

#Set TimeZone
os.environ['TZ'] = 'Asia/Manila'
time.tzset()

#Current Date Time
now = datetime.datetime.now()

timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
dates = now.strftime('%Y-%m-%d')

#Set Database Connection
c, conn = connection()

#set Database connection Failover
e, catch = failover()

#Get ID
def get_id(uname):

	if conn.open:
		date = c.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

		data = c.fetchone()[0]

		return data
	else:
		date = e.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

		data = e.fetchone()[0]

		return data

#Check Username
def check_username(uname):

	if conn.open:
		date = c.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

		data = c.fetchone()[4]

		return data
	else:
		date = e.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

		data = e.fetchone()[4]

		return data

#Check if Usernamme is available
def unique_username(uname):

	if conn.open:
		data = c.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

		return data
	else:
		data = e.execute("SELECT * FROM users WHERE username = (%s)",(uname,))

		return data

def get_role():
	if conn.open:
		data = c.execute("SELECT * FROM py_role WHERE rolename != 'super admin'")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM py_role WHERE rolename != 'super admin'")
		data = e.fetchall()
		return data


#Check if Usernamme is available
def unique_email(email):

	if conn.open:
		data = c.execute("SELECT * FROM users WHERE email = (%s)",(email,))

		return data
	else:
		data = e.execute("SELECT * FROM users WHERE email = (%s)",(email,))

		return data

#Log User Loggedin
def tracked_loggedin(uid):

	if conn.open:
		data = c.execute("INSERT INTO py_loggedin_activity (userid, loggedin) VALUES (%s, %s)",(uid,timestamp))

		conn.commit()
	else:
		data = e.execute("INSERT INTO py_loggedin_activity (userid, loggedin) VALUES (%s, %s)",(uid,timestamp))

		catch.commit()

#Update Logout
def logout_update(uid):

	if conn.open:
		data = c.execute("UPDATE py_loggedin_activity SET loggedout = %s WHERE userid = %s AND loggedout IS NULL",(timestamp,uid))

		conn.commit()
	else:
		data = e.execute("UPDATE py_loggedin_activity SET loggedout = %s WHERE userid = %s AND loggedout IS NULL",(timestamp,uid))

		catch.commit()

def register(uname,password,email,firstname,lastname,role,address):

	if conn.open:
		c.execute("INSERT INTO users (username, password, email, firstname, lastname, role, address, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(thwart(uname), thwart(password), thwart(email), thwart(firstname), thwart(lastname), thwart(role), thwart(address), timestamp))

		conn.commit()
	else:
		e.execute("INSERT INTO users (username, password, email, firstname, lastname, role, address, date_created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",(thwart(uname), thwart(password), thwart(email), thwart(firstname), thwart(lastname), thwart(role), thwart(address), timestamp))

		catch.commit()

def msgme(name,msg):

	if conn.open:
		c.execute("INSERT INTO msg_me (name, msg, created_at) VALUES (%s, %s, %s)",(thwart(name), thwart(msg), timestamp))

		conn.commit()
	else:
		e.execute("INSERT INTO msg_me (name, msg, created_at) VALUES (%s, %s, %s)",(thwart(name), thwart(msg), timestamp))

		catch.commit()

def webhook():

	if conn.open:
		c.execute("INSERT INTO webhooks (url, ip, dates, created_at) VALUES (%s, %s, %s, %s)",(thwart(request.url), thwart(request.remote_addr), dates, timestamp))

		conn.commit()
	else:
		e.execute("INSERT INTO webhooks (url, ip, dates, created_at) VALUES (%s, %s, %s, %s)",(thwart(request.url), thwart(request.remote_addr), dates, timestamp))

		catch.commit()

def unreadmsg():

	if conn.open:
		data = c.execute("SELECT * FROM msg_me WHERE unread IS NULL ")
		count = c.rowcount
		return data
	else:
		data = e.execute("SELECT * FROM msg_me WHERE unread IS NULL ")
		count = c.rowcount
		return data

def getUnreadmsg():

	if conn.open:
		data = c.execute("SELECT * FROM msg_me WHERE unread IS NULL ")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM msg_me WHERE unread IS NULL ")
		data = e.fetchall()
		return data

def getdays():

	if conn.open:
		data = c.execute("SELECT DISTINCT dates FROM webhooks WHERE dates >= DATE(NOW()) - INTERVAL 7 DAY")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT DISTINCT dates FROM webhooks WHERE dates >= DATE(NOW()) - INTERVAL 7 DAY")
		data = e.fetchall()
		return data

def countVisitors():

	if conn.open:
		data = c.execute("SELECT DISTINCT ip FROM webhooks WHERE dates = (%s)",(dates,))
		count = c.rowcount
		return count
	else:
		data = e.execute("SELECT DISTINCT ip FROM webhooks WHERE dates = (%s)",(dates,))
		count = e.rowcount
		return count


def getVisitors():

	if conn.open:
		data = c.execute("SELECT * FROM webhooks ORDER BY created_at DESC")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM webhooks ORDER BY created_at DESC")
		data = e.fetchall()
		return data

def visitorCountAll():

	if conn.open:
		data = c.execute("SELECT DISTINCT ip FROM webhooks")
		count = c.rowcount
		return count
	else:
		data = e.execute("SELECT DISTINCT ip FROM webhooks")
		count = e.rowcount
		return count

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

#Current Date Time
now = datetime.datetime.now()

timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
dates = now.strftime('%Y-%m-%d')
y = now.year
yMonth = now.strftime('%Y-%m')

intip = '1'

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
		c.execute("INSERT INTO msg_me (name, msg, ip, created_at) VALUES (%s, %s, %s, %s)",(thwart(name), thwart(msg), thwart(request.remote_addr), timestamp))

		conn.commit()
	else:
		e.execute("INSERT INTO msg_me (name, msg, ip, created_at) VALUES (%s, %s, %s, %s)",(thwart(name), thwart(msg), thwart(request.remote_addr), timestamp))

		catch.commit()

def webhook():

	if conn.open:
		c.execute("INSERT INTO webhooks (url, ip, dates, created_at, y_month, year) VALUES (%s, %s, %s, %s, %s, %s)",(thwart(request.url), thwart(request.remote_addr), dates, timestamp, yMonth, y))

		conn.commit()
	else:
		e.execute("INSERT INTO webhooks (url, ip, dates, created_at, y_month, year) VALUES (%s, %s, %s, %s, %s, %s)",(thwart(request.url), thwart(request.remote_addr), dates, timestamp, yMonth, y))

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
		data = c.execute("SELECT * FROM msg_me WHERE unread IS NULL")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM msg_me WHERE unread IS NULL")
		data = e.fetchall()
		return data

def getAllMessage():

	if conn.open:
		data = c.execute("SELECT * FROM msg_me ORDER BY created_at DESC ")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM msg_me ORDER BY created_at DESC ")
		data = e.fetchall()
		return data

def getMessage(msgid):
	if conn.open:
		data = c.execute("SELECT * FROM msg_me WHERE id = (%s)",(msgid,))
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM msg_me WHERE id = (%s)",(msgid,))
		data = e.fetchall()
		return data

def updateMessage(msgid):
	if conn.open:
		data = c.execute("UPDATE `msg_me` SET `unread` = '1' WHERE id = (%s)",(msgid,))
		data = c.fetchall()
		return data
	else:
		data = e.execute("UPDATE `msg_me` SET `unread` = '1' WHERE id = (%s)",(msgid,))
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

def block_ip():

	if conn.open:
		data = c.execute("SELECT * FROM block_ip WHERE block = 1")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM block_ip WHERE block = 1")
		data = e.fetchall()
		return data

def getAllBlock_ip():

	if conn.open:
		data = c.execute("SELECT * FROM block_ip")
		data = c.fetchall()
		return data
	else:
		data = e.execute("SELECT * FROM block_ip")
		data = e.fetchall()
		return data


def check_ip(clientip):

	if conn.open:
		data = c.execute("SELECT * FROM block_ip WHERE ip = (%s)",(clientip,))

		return data
	else:
		data = e.execute("SELECT * FROM block_ip WHERE ip = (%s)",(clientip,))

		return data

def block_client_ip(clientip):

	if conn.open:
		c.execute("INSERT INTO block_ip (ip, block, created_at) VALUES (%s, %s, %s)",(thwart(clientip), thwart(intip), timestamp))

		conn.commit()
	else:
		e.execute("INSERT INTO webhooks (ip, block, created_at) VALUES (%s, %s, %s)",(thwart(clientip), thwart(intip), timestamp))

		catch.commit()

def getIDBlock_ip(blockid):

	if conn.open:
		data = c.execute("SELECT * FROM block_ip WHERE id = (%s)",(blockid,))

		return data
	else:
		data = e.execute("SELECT * FROM block_ip WHERE id = (%s)",(blockid,))

		return data

def updateBlock_ip(blockid,cbid):

	if conn.open:
		data = c.execute("UPDATE block_ip SET block = %s WHERE id = %s",(cbid,blockid))

		conn.commit()
	else:
		data = e.execute("UPDATE block_ip SET block = %s WHERE id = %s",(cbid,blockid))

		catch.commit()

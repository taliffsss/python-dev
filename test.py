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

#Set Database Connection
c, conn = connection()

def get_role():
	data = c.execute("SELECT * FROM py_role WHERE rolename != 'super admin'")
	data = c.fetchall()
	return data

role = get_role()
for row in role:
	print(row[1])
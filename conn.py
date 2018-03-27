import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "@gLip@y113",
                           db = "python")
    c = conn.cursor()

    return c, conn

def failover():
    catch = MySQLdb.connect(host="localhost",
                           user = "taliffsss",
                           passwd = "@n0nym0us15",
                           db = "python")
    e = catch.cursor()

    return e, catch

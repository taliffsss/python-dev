from conn import connection, failover

#Set Database Connection
c, conn = connection()

#set Database connection Failover
e, catch = failover()

data = c.execute("SELECT DISTINCT ip FROM webhooks")
count = c.rowcount

print(count)

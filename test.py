from conn import connection, failover

#Set Database Connection
c, conn = connection()

#set Database connection Failover
e, catch = failover()

data = c.execute("SELECT ip FROM block_ip")
count = c.fetchall()
output = count.strip('()')
print(output)

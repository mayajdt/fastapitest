import sqlite3

con = sqlite3.connect("fastapitest.db")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS ping_results(url, ip, packets_sent, packets_rec, time)")
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())

con.close()
"""Check the connection to the lab SQL Server."""
from util import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT @@VERSION, DB_NAME(), SUSER_NAME();")
version, db, user = cur.fetchone()
print(f"Connected ✅  database={db}  login={user}")
print(version.splitlines()[0])
conn.close()

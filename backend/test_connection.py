"""Quick connection test - run this directly to verify credentials"""
import pymssql

# Edit these to match exactly what's in Azure Portal
SERVER = "cischurch-sql.database.windows.net"
DATABASE = "ASC"
USERNAME = "SQLadmin"
PASSWORD = "Church@123"
PORT = 1433

print(f"Testing: {USERNAME}@{SERVER}:{PORT}/{DATABASE}")
print(f"Password: {PASSWORD}")

try:
    conn = pymssql.connect(
        server=SERVER,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        timeout=10
    )
    cursor = conn.cursor()
    cursor.execute("SELECT @@VERSION")
    print("SUCCESS:", cursor.fetchone()[0][:50])
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")

# Also try without specifying database (in case DB name is wrong)
print("\nTrying without database name...")
try:
    conn = pymssql.connect(
        server=SERVER,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        timeout=10
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    print("Available databases:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}")
    conn.close()
except Exception as e:
    print(f"FAILED: {e}")

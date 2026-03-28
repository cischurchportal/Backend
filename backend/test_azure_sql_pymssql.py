"""
Azure SQL Server Connection Test Script (using pymssql - no ODBC required)
Tests connection to Azure SQL Database
"""

import pymssql
import sys
from datetime import datetime

# Connection parameters
SERVER = 'cischurch-sql.database.windows.net'
DATABASE = 'cischurch-sql-db'
USERNAME = 'SQLadmin'  # Without @server suffix for pymssql
PASSWORD = 'qwertyuiop.1'
PORT = 1433

def test_connection():
    """Test Azure SQL Server connection using pymssql"""
    print("=" * 60)
    print("Azure SQL Server Connection Test (pymssql)")
    print("=" * 60)
    print(f"Server: {SERVER}")
    print(f"Database: {DATABASE}")
    print(f"Username: {USERNAME}")
    print(f"Port: {PORT}")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 60)
    
    try:
        print("\n[1/4] Attempting to connect to Azure SQL Server...")
        conn = pymssql.connect(
            server=SERVER,
            user=USERNAME,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            timeout=30,
            login_timeout=30,
            as_dict=False
        )
        print("✓ Connection successful!")
        
        print("\n[2/4] Creating cursor...")
        cursor = conn.cursor()
        print("✓ Cursor created!")
        
        print("\n[3/4] Testing query execution (SELECT @@VERSION)...")
        cursor.execute("SELECT @@VERSION as version")
        row = cursor.fetchone()
        print("✓ Query executed successfully!")
        print(f"\nSQL Server Version:\n{row[0]}")
        
        print("\n[4/4] Listing available tables...")
        cursor.execute("""
            SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        tables = cursor.fetchall()
        if tables:
            print(f"\n✓ Found {len(tables)} table(s):")
            for table in tables:
                print(f"  - {table[0]}.{table[1]} ({table[2]})")
        else:
            print("\n⚠ No tables found in database")
        
        # Test a simple query
        print("\n[BONUS] Testing simple SELECT query...")
        cursor.execute("SELECT 1 + 1 AS result")
        result = cursor.fetchone()
        print(f"✓ Query result: 1 + 1 = {result[0]}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✓ CONNECTION TEST PASSED - All operations successful!")
        print("=" * 60)
        return True
        
    except pymssql.Error as e:
        print("\n" + "=" * 60)
        print("✗ CONNECTION TEST FAILED")
        print("=" * 60)
        print(f"\nError Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        
        error_str = str(e).lower()
        
        if "login failed" in error_str or "authentication" in error_str:
            print("\n⚠ Authentication Issue Detected!")
            print("\nPossible solutions:")
            print("1. Verify username and password are correct")
            print("2. Check Azure SQL firewall rules - add your IP address:")
            print("   Azure Portal > SQL Server > Networking > Firewall rules")
            print("3. Verify the user has access to the database")
            print("4. Try username with @server: 'SQLadmin@cischurch-sql'")
        
        elif "timeout" in error_str or "connection" in error_str:
            print("\n⚠ Connection Issue Detected!")
            print("\nPossible solutions:")
            print("1. Check your internet connection")
            print("2. Verify firewall rules in Azure Portal allow your IP")
            print("3. Check if server name is correct")
            print("4. Ensure port 1433 is not blocked by local firewall")
        
        elif "database" in error_str:
            print("\n⚠ Database Access Issue!")
            print("\nPossible solutions:")
            print("1. Verify database name is correct")
            print("2. Check if user has access to this specific database")
        
        print("\n" + "=" * 60)
        return False
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ UNEXPECTED ERROR")
        print("=" * 60)
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        print("=" * 60)
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)

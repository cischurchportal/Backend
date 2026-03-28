"""
Azure SQL Server Connection Test Script
Tests connection to Azure SQL Database using pyodbc
"""

import pyodbc
import sys
from datetime import datetime

# Connection parameters from your JDBC string
SERVER = 'cischurch-sql.database.windows.net'
DATABASE = 'cischurch-sql-db'
USERNAME = 'SQLadmin@cischurch-sql'
PASSWORD = 'qwertyuiop.1'  # Replace with actual password if different
DRIVER = '{ODBC Driver 18 for SQL Server}'  # or '{ODBC Driver 17 for SQL Server}'

def test_connection():
    """Test Azure SQL Server connection"""
    print("=" * 60)
    print("Azure SQL Server Connection Test")
    print("=" * 60)
    print(f"Server: {SERVER}")
    print(f"Database: {DATABASE}")
    print(f"Username: {USERNAME}")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 60)
    
    connection_string = (
        f"DRIVER={DRIVER};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={USERNAME};"
        f"PWD={PASSWORD};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    
    try:
        print("\n[1/4] Attempting to connect to Azure SQL Server...")
        conn = pyodbc.connect(connection_string)
        print("✓ Connection successful!")
        
        print("\n[2/4] Creating cursor...")
        cursor = conn.cursor()
        print("✓ Cursor created!")
        
        print("\n[3/4] Testing query execution (SELECT @@VERSION)...")
        cursor.execute("SELECT @@VERSION as version")
        row = cursor.fetchone()
        print("✓ Query executed successfully!")
        print(f"\nSQL Server Version:\n{row.version}")
        
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
                print(f"  - {table.TABLE_SCHEMA}.{table.TABLE_NAME} ({table.TABLE_TYPE})")
        else:
            print("\n⚠ No tables found in database")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✓ CONNECTION TEST PASSED - All operations successful!")
        print("=" * 60)
        return True
        
    except pyodbc.Error as e:
        print("\n" + "=" * 60)
        print("✗ CONNECTION TEST FAILED")
        print("=" * 60)
        print(f"\nError Type: {type(e).__name__}")
        print(f"Error Message: {str(e)}")
        
        if "ODBC Driver" in str(e):
            print("\n⚠ ODBC Driver Issue Detected!")
            print("\nPossible solutions:")
            print("1. Install ODBC Driver 18 for SQL Server:")
            print("   https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
            print("\n2. Or try changing DRIVER to '{ODBC Driver 17 for SQL Server}'")
            print("   in the script if you have version 17 installed")
        
        elif "Login failed" in str(e) or "authentication" in str(e).lower():
            print("\n⚠ Authentication Issue Detected!")
            print("\nPossible solutions:")
            print("1. Verify username and password are correct")
            print("2. Check if firewall rules allow your IP address")
            print("3. Verify the user has access to the database")
        
        elif "timeout" in str(e).lower():
            print("\n⚠ Connection Timeout!")
            print("\nPossible solutions:")
            print("1. Check your internet connection")
            print("2. Verify firewall rules in Azure Portal")
            print("3. Check if server name is correct")
        
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

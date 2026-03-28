"""
Azure SQL Server Connection Test - Flexible Authentication
Tries multiple username formats and provides detailed diagnostics

Usage:
    Set environment variables or edit .env file:
    - AZURE_SQL_SERVER
    - AZURE_SQL_DATABASE
    - AZURE_SQL_USERNAME
    - AZURE_SQL_PASSWORD
    
    Or run with defaults for cischurch-sql
"""

import pymssql
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connection parameters (with defaults)
SERVER = os.getenv('AZURE_SQL_SERVER', 'cischurch-sql.database.windows.net')
DATABASE = os.getenv('AZURE_SQL_DATABASE', 'cischurch-sql-db')
PASSWORD = os.getenv('AZURE_SQL_PASSWORD', 'qwertyuiop.1')
PORT = int(os.getenv('AZURE_SQL_PORT', '1433'))
BASE_USERNAME = os.getenv('AZURE_SQL_USERNAME', 'SQLadmin')

# Different username formats to try
SERVER_NAME = SERVER.split('.')[0]  # Extract 'cischurch-sql' from full domain
USERNAME_FORMATS = [
    f'{BASE_USERNAME}@{SERVER_NAME}',  # Format from JDBC string
    BASE_USERNAME,                      # Simple format
]

def test_connection_with_username(username):
    """Test connection with specific username format"""
    try:
        conn = pymssql.connect(
            server=SERVER,
            user=username,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            timeout=15,
            login_timeout=15
        )
        return conn, None
    except Exception as e:
        return None, str(e)

def main():
    print("=" * 70)
    print("Azure SQL Server Connection Test - Flexible Authentication")
    print("=" * 70)
    print(f"Server: {SERVER}")
    print(f"Database: {DATABASE}")
    print(f"Port: {PORT}")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 70)
    
    print("\n🔍 Testing different username formats...\n")
    
    successful_connection = None
    successful_username = None
    
    for i, username in enumerate(USERNAME_FORMATS, 1):
        print(f"[Attempt {i}/{len(USERNAME_FORMATS)}] Testing username: '{username}'")
        conn, error = test_connection_with_username(username)
        
        if conn:
            print(f"  ✓ SUCCESS with username: '{username}'")
            successful_connection = conn
            successful_username = username
            break
        else:
            print(f"  ✗ Failed: {error[:100]}...")
    
    if not successful_connection:
        print("\n" + "=" * 70)
        print("✗ ALL CONNECTION ATTEMPTS FAILED")
        print("=" * 70)
        print("\n🔧 TROUBLESHOOTING STEPS:\n")
        print("1. VERIFY CREDENTIALS:")
        print("   - Check if password is correct: 'qwertyuiop.1'")
        print("   - Verify admin username in Azure Portal")
        print()
        print("2. CHECK FIREWALL RULES:")
        print("   - Go to Azure Portal > SQL Server > Networking")
        print("   - Add your current IP address to firewall rules")
        print("   - Or temporarily enable 'Allow Azure services' for testing")
        print()
        print("3. VERIFY SERVER STATUS:")
        print("   - Ensure SQL Server is running in Azure Portal")
        print("   - Check if there are any service issues")
        print()
        print("4. CHECK USER PERMISSIONS:")
        print("   - Verify user has access to the specific database")
        print("   - Check if user account is active")
        print()
        print("5. TRY AZURE DATA STUDIO:")
        print("   - Download: https://aka.ms/azuredatastudio")
        print("   - Test connection manually to verify credentials")
        print("=" * 70)
        return False
    
    # Connection successful - run tests
    print("\n" + "=" * 70)
    print(f"✓ CONNECTED SUCCESSFULLY with username: '{successful_username}'")
    print("=" * 70)
    
    try:
        cursor = successful_connection.cursor()
        
        print("\n[TEST 1] SQL Server Version:")
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"  {version[:100]}...")
        
        print("\n[TEST 2] Current Database:")
        cursor.execute("SELECT DB_NAME()")
        db_name = cursor.fetchone()[0]
        print(f"  ✓ Connected to database: {db_name}")
        
        print("\n[TEST 3] Server Name:")
        cursor.execute("SELECT @@SERVERNAME")
        server_name = cursor.fetchone()[0]
        print(f"  ✓ Server name: {server_name}")
        
        print("\n[TEST 4] Current User:")
        cursor.execute("SELECT CURRENT_USER")
        current_user = cursor.fetchone()[0]
        print(f"  ✓ Logged in as: {current_user}")
        
        print("\n[TEST 5] Listing Tables:")
        cursor.execute("""
            SELECT 
                TABLE_SCHEMA, 
                TABLE_NAME, 
                TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_TYPE IN ('BASE TABLE', 'VIEW')
            ORDER BY TABLE_SCHEMA, TABLE_NAME
        """)
        
        tables = cursor.fetchall()
        if tables:
            print(f"  ✓ Found {len(tables)} table(s)/view(s):")
            for schema, name, ttype in tables[:20]:  # Show first 20
                print(f"    - {schema}.{name} ({ttype})")
            if len(tables) > 20:
                print(f"    ... and {len(tables) - 20} more")
        else:
            print("  ⚠ No tables found (database might be empty)")
        
        print("\n[TEST 6] Simple Calculation:")
        cursor.execute("SELECT 2 + 2 AS result")
        result = cursor.fetchone()[0]
        print(f"  ✓ Query test: 2 + 2 = {result}")
        
        cursor.close()
        successful_connection.close()
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        print(f"\n💡 Use this username format in your application: '{successful_username}'")
        print("=" * 70)
        return True
        
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        successful_connection.close()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

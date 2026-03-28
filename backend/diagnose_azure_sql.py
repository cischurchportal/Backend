"""
Comprehensive Azure SQL Connection Diagnostics
Tests network connectivity, DNS resolution, and authentication
"""

import socket
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERVER = os.getenv('AZURE_SQL_SERVER', 'cischurch-sql.database.windows.net')
DATABASE = os.getenv('AZURE_SQL_DATABASE', 'cischurch-sql-db')
USERNAME = os.getenv('AZURE_SQL_USERNAME', 'SQLadmin')
PASSWORD = os.getenv('AZURE_SQL_PASSWORD', 'qwertyuiop.1')
PORT = int(os.getenv('AZURE_SQL_PORT', '1433'))

def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

def test_dns_resolution():
    """Test if server hostname resolves"""
    print_header("TEST 1: DNS Resolution")
    try:
        ip_address = socket.gethostbyname(SERVER)
        print(f"✓ DNS Resolution successful")
        print(f"  Server: {SERVER}")
        print(f"  IP Address: {ip_address}")
        return True
    except socket.gaierror as e:
        print(f"✗ DNS Resolution failed: {e}")
        print(f"  Cannot resolve hostname: {SERVER}")
        return False

def test_port_connectivity():
    """Test if port 1433 is reachable"""
    print_header("TEST 2: Port Connectivity")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((SERVER, PORT))
        sock.close()
        
        if result == 0:
            print(f"✓ Port {PORT} is OPEN and reachable")
            print(f"  This means firewall allows your connection")
            return True
        else:
            print(f"✗ Port {PORT} is CLOSED or BLOCKED")
            print(f"  Error code: {result}")
            print(f"\n🔧 FIREWALL ISSUE DETECTED:")
            print(f"  1. Go to Azure Portal")
            print(f"  2. Navigate to: SQL Server > {SERVER.split('.')[0]}")
            print(f"  3. Click 'Networking' or 'Firewalls and virtual networks'")
            print(f"  4. Add your current IP address")
            print(f"  5. Or enable 'Allow Azure services and resources to access this server'")
            return False
    except Exception as e:
        print(f"✗ Connection test failed: {e}")
        return False

def test_pymssql_connection():
    """Test actual database connection"""
    print_header("TEST 3: Database Authentication")
    
    try:
        import pymssql
    except ImportError:
        print("✗ pymssql not installed")
        print("  Run: pip install pymssql")
        return False
    
    # Try different username formats
    username_formats = [
        USERNAME,
        f"{USERNAME}@{SERVER.split('.')[0]}",
    ]
    
    for i, username in enumerate(username_formats, 1):
        print(f"\n[Attempt {i}] Username: '{username}'")
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
            print(f"  ✓ Authentication SUCCESSFUL!")
            
            # Quick test query
            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]
            print(f"  ✓ Connected to: {version[:80]}...")
            
            cursor.close()
            conn.close()
            return True
            
        except pymssql.OperationalError as e:
            error_msg = str(e)
            print(f"  ✗ Failed: {error_msg[:100]}")
            
            # Analyze error
            if "18456" in error_msg:
                print(f"\n  🔧 LOGIN FAILED (Error 18456):")
                print(f"     - Username or password is incorrect")
                print(f"     - Or SQL Authentication is disabled")
                print(f"     - Or user doesn't have access to database '{DATABASE}'")
            elif "40615" in error_msg or "firewall" in error_msg.lower():
                print(f"\n  🔧 FIREWALL BLOCKED (Error 40615):")
                print(f"     - Your IP address is not in the firewall rules")
            elif "timeout" in error_msg.lower():
                print(f"\n  🔧 TIMEOUT:")
                print(f"     - Server might be unreachable")
                print(f"     - Or firewall is blocking silently")
        except Exception as e:
            print(f"  ✗ Unexpected error: {e}")
    
    return False

def check_azure_cli():
    """Check if Azure CLI is available"""
    print_header("TEST 4: Azure CLI Check (Optional)")
    try:
        import subprocess
        result = subprocess.run(['az', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            print("✓ Azure CLI is installed")
            print("\n💡 You can use Azure CLI to check your SQL Server:")
            print(f"   az sql server show --name {SERVER.split('.')[0]} --resource-group <your-rg>")
            return True
        else:
            print("✗ Azure CLI not found")
            return False
    except:
        print("ℹ Azure CLI not installed (optional)")
        print("  Install from: https://aka.ms/installazurecliwindows")
        return False

def main():
    print("=" * 70)
    print("Azure SQL Connection Diagnostics")
    print("=" * 70)
    print(f"Timestamp: {datetime.now()}")
    print(f"Server: {SERVER}")
    print(f"Database: {DATABASE}")
    print(f"Username: {USERNAME}")
    print(f"Port: {PORT}")
    
    # Run all tests
    dns_ok = test_dns_resolution()
    port_ok = test_port_connectivity()
    auth_ok = test_pymssql_connection()
    check_azure_cli()
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    print(f"DNS Resolution:    {'✓ PASS' if dns_ok else '✗ FAIL'}")
    print(f"Port Connectivity: {'✓ PASS' if port_ok else '✗ FAIL'}")
    print(f"Authentication:    {'✓ PASS' if auth_ok else '✗ FAIL'}")
    
    if auth_ok:
        print("\n🎉 All tests passed! Your connection is working.")
    elif not port_ok:
        print("\n⚠ PRIMARY ISSUE: Firewall is blocking your connection")
        print("   Fix the firewall rules in Azure Portal first")
    elif not auth_ok:
        print("\n⚠ PRIMARY ISSUE: Authentication failed")
        print("   Check your username and password in Azure Portal")
    
    print("=" * 70)
    
    return auth_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

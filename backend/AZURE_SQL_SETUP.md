# Azure SQL Server Setup Guide

## Current Configuration
- **Server**: cischurch-sql.database.windows.net
- **Database**: cischurch-sql-db
- **Admin User**: SQLadmin
- **Port**: 1433

## 🔥 FIREWALL CONFIGURATION (REQUIRED)

Your Azure SQL Server currently blocks external connections. Choose one option:

### Option 1: Allow Azure Services (Recommended for Production)
**Best for**: Azure Functions, App Services, and other Azure-hosted applications

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: SQL servers → cischurch-sql
3. Click: **Networking** (left sidebar)
4. Under "Exceptions":
   - ✅ Enable: **"Allow Azure services and resources to access this server"**
5. Click **Save**

✅ **Pros**: Secure, allows Azure Functions to connect
❌ **Cons**: Doesn't allow local development without additional rules

---

### Option 2: Allow Specific IP Addresses (Recommended for Development)
**Best for**: Team members working locally

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to: SQL servers → cischurch-sql → Networking
3. Click **"Add your client IP address"** (adds your current IP)
4. Or manually add IP ranges:
   - Rule name: `Developer1`
   - Start IP: `xxx.xxx.xxx.xxx`
   - End IP: `xxx.xxx.xxx.xxx`
5. Click **Save**

✅ **Pros**: Secure, controlled access
❌ **Cons**: Need to update when IP changes

---

### Option 3: Allow All IP Addresses (NOT RECOMMENDED)
**⚠️ SECURITY WARNING**: Only use for testing/development

1. Go to Azure Portal → SQL servers → cischurch-sql → Networking
2. Add firewall rule:
   - Rule name: `AllowAll`
   - Start IP: `0.0.0.0`
   - End IP: `255.255.255.255`
3. Click **Save**

❌ **Security Risk**: Anyone can attempt to connect
✅ **Use Case**: Quick testing only

**If using this option, ensure**:
- Strong password (current: qwertyuiop.1 - consider changing!)
- Monitor connection logs
- Disable when not needed

---

## 🧪 TESTING CONNECTION

### 1. Install Dependencies
```bash
cd Backend/backend
pip install pymssql python-dotenv
```

### 2. Configure Environment Variables
Edit `Backend/backend/.env`:
```env
AZURE_SQL_SERVER=cischurch-sql.database.windows.net
AZURE_SQL_DATABASE=cischurch-sql-db
AZURE_SQL_USERNAME=SQLadmin
AZURE_SQL_PASSWORD=qwertyuiop.1
AZURE_SQL_PORT=1433
```

### 3. Run Connection Test
```bash
python test_azure_sql_flexible.py
```

**Expected Output** (if successful):
```
✓ CONNECTED SUCCESSFULLY with username: 'SQLadmin@cischurch-sql'
[TEST 1] SQL Server Version: ...
[TEST 2] Current Database: cischurch-sql-db
✓ ALL TESTS PASSED!
```

---

## 🔧 TROUBLESHOOTING

### Error: "Login failed for user"
**Causes**:
1. ❌ Firewall blocking your IP → Add IP to firewall rules
2. ❌ Wrong password → Verify in Azure Portal
3. ❌ Wrong username format → Script tries both formats automatically

**Solution**:
```bash
# Check firewall rules in Azure Portal
# Try resetting password in: SQL servers → cischurch-sql → Settings → SQL databases
```

### Error: "Connection timeout"
**Causes**:
1. ❌ Firewall blocking connection
2. ❌ Server name incorrect
3. ❌ Local firewall blocking port 1433

**Solution**:
```bash
# Test connectivity
ping cischurch-sql.database.windows.net

# Check if port 1433 is open (Windows)
Test-NetConnection -ComputerName cischurch-sql.database.windows.net -Port 1433
```

### Error: "Cannot open database"
**Causes**:
1. ❌ Database name incorrect
2. ❌ User doesn't have access to database

**Solution**:
- Verify database name in Azure Portal
- Check user permissions

---

## 📦 USING IN YOUR APPLICATION

### Install Package
```bash
pip install pymssql
```

### Example Connection Code
```python
import pymssql
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Azure SQL
conn = pymssql.connect(
    server=os.getenv('AZURE_SQL_SERVER'),
    user=os.getenv('AZURE_SQL_USERNAME'),
    password=os.getenv('AZURE_SQL_PASSWORD'),
    database=os.getenv('AZURE_SQL_DATABASE'),
    port=int(os.getenv('AZURE_SQL_PORT', 1433))
)

cursor = conn.cursor()
cursor.execute("SELECT @@VERSION")
print(cursor.fetchone()[0])

cursor.close()
conn.close()
```

---

## 🔐 SECURITY BEST PRACTICES

### 1. Change Default Password
Current password `qwertyuiop.1` is weak. Change it:
1. Azure Portal → SQL servers → cischurch-sql
2. Settings → SQL databases → cischurch-sql-db
3. Set server admin → Reset password

### 2. Use Environment Variables
✅ **DO**: Store credentials in `.env` (already configured)
❌ **DON'T**: Hardcode credentials in code

### 3. Use Azure AD Authentication (Advanced)
Instead of SQL authentication, use Azure Active Directory:
- More secure
- No password management
- Better audit logs

### 4. Enable Auditing
Azure Portal → SQL servers → cischurch-sql → Security → Auditing

### 5. Regular Backups
Azure SQL has automatic backups, but verify:
- Azure Portal → SQL databases → cischurch-sql-db → Backups

---

## 📊 MONITORING

### View Connection Logs
Azure Portal → SQL servers → cischurch-sql → Monitoring → Metrics

### Check Active Connections
```sql
SELECT 
    DB_NAME(dbid) as DatabaseName,
    COUNT(dbid) as NumberOfConnections,
    loginame as LoginName
FROM sys.sysprocesses
WHERE dbid > 0
GROUP BY dbid, loginame
```

---

## 🚀 NEXT STEPS

1. ✅ Configure firewall (Option 1 or 2 above)
2. ✅ Run `test_azure_sql_flexible.py` to verify connection
3. ✅ Consider changing the default password
4. ✅ Integrate with your Azure Functions application
5. ✅ Set up monitoring and alerts

---

## 📞 SUPPORT

If you continue having issues:
1. Check Azure Service Health: https://status.azure.com
2. Review Azure SQL documentation: https://docs.microsoft.com/azure/sql-database/
3. Check firewall rules are saved and active (can take 1-2 minutes)

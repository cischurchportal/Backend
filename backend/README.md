# Church App Backend - Azure Functions

A clean, well-structured FastAPI backend deployed as an Azure Function App (Python 3.11) following best practices with proper separation of concerns.

## Architecture

The backend follows a clean architecture pattern with the following layers:

```
backend/
├── app/
│   ├── controllers/        # API endpoints and request handling
│   ├── services/          # Business logic
│   ├── repositories/      # Data access layer
│   ├── models/           # Pydantic schemas
│   └── utils/            # Utility functions
├── main.py               # FastAPI application entry point
└── requirements.txt      # Python dependencies
```

## Layers Explained

### 1. Controllers (`app/controllers/`)
- Handle HTTP requests and responses
- Input validation and serialization
- Route definitions
- Error handling

**Files:**
- `auth_controller.py` - Authentication endpoints
- `member_controller.py` - Member management endpoints
- `event_controller.py` - Event management endpoints
- `ministry_controller.py` - Ministry management endpoints
- `donation_controller.py` - Donation management endpoints

### 2. Services (`app/services/`)
- Business logic implementation
- Data validation and processing
- Orchestration between repositories
- Complex operations and calculations

**Files:**
- `auth_service.py` - Authentication and user management
- `member_service.py` - Member operations and statistics
- `event_service.py` - Event management and scheduling
- `ministry_service.py` - Ministry operations and member assignments
- `donation_service.py` - Financial operations and reporting

### 3. Repositories (`app/repositories/`)
- Data access layer
- CRUD operations
- Database abstraction
- Query implementations

**Files:**
- `base_repository.py` - Common database operations
- `user_repository.py` - User data access
- `member_repository.py` - Member data access
- `event_repository.py` - Event data access
- `ministry_repository.py` - Ministry data access
- `donation_repository.py` - Donation data access

### 4. Models (`app/models/`)
- Pydantic schemas for request/response validation
- Data transfer objects
- API documentation

**Files:**
- `schemas.py` - All Pydantic models

### 5. Utils (`app/utils/`)
- Helper functions
- Common utilities
- Security functions
- Validation helpers

**Files:**
- `security.py` - Password hashing and token generation
- `validators.py` - Input validation functions
- `responses.py` - Standardized API responses

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/admin/login` - Admin login
- `GET /api/auth/profile/{user_id}` - Get user profile

### Members
- `GET /api/members/` - Get all members
- `GET /api/members/active` - Get active members
- `GET /api/members/search?q={term}` - Search members
- `GET /api/members/statistics` - Get membership statistics
- `GET /api/members/{id}` - Get specific member
- `POST /api/members/` - Create new member
- `PUT /api/members/{id}` - Update member
- `DELETE /api/members/{id}` - Delete member
- `GET /api/members/{id}/ministries` - Get member's ministries
- `POST /api/members/{id}/ministries/{name}` - Add member to ministry
- `DELETE /api/members/{id}/ministries/{name}` - Remove member from ministry

### Events
- `GET /api/events/` - Get all events
- `GET /api/events/upcoming` - Get upcoming events
- `GET /api/events/this-week` - Get this week's events
- `GET /api/events/this-month` - Get this month's events
- `GET /api/events/by-type/{type}` - Get events by type
- `GET /api/events/statistics` - Get event statistics
- `GET /api/events/{id}` - Get specific event
- `POST /api/events/` - Create new event
- `PUT /api/events/{id}` - Update event
- `DELETE /api/events/{id}` - Delete event
- `POST /api/events/{id}/register` - Register for event
- `POST /api/events/{id}/unregister` - Unregister from event

### Ministries
- `GET /api/ministries/` - Get all ministries
- `GET /api/ministries/active` - Get active ministries
- `GET /api/ministries/statistics` - Get ministry statistics
- `GET /api/ministries/{id}` - Get specific ministry
- `GET /api/ministries/{id}/details` - Get ministry with member details
- `POST /api/ministries/` - Create new ministry
- `PUT /api/ministries/{id}` - Update ministry
- `DELETE /api/ministries/{id}` - Delete ministry
- `POST /api/ministries/{id}/members/{member_id}` - Add member to ministry
- `DELETE /api/ministries/{id}/members/{member_id}` - Remove member from ministry
- `GET /api/ministries/leader/{leader_id}` - Get ministries by leader
- `GET /api/ministries/member/{member_id}` - Get member's ministries

### Donations
- `GET /api/donations/` - Get all donations
- `GET /api/donations/statistics` - Get donation statistics
- `GET /api/donations/fund-totals` - Get totals by fund
- `GET /api/donations/monthly-totals/{year}` - Get monthly totals
- `GET /api/donations/by-member/{member_id}` - Get donations by member
- `GET /api/donations/by-fund/{fund}` - Get donations by fund
- `GET /api/donations/by-date-range` - Get donations in date range
- `GET /api/donations/member-summary/{member_id}` - Get member donation summary
- `GET /api/donations/{id}` - Get specific donation
- `POST /api/donations/` - Create new donation
- `PUT /api/donations/{id}` - Update donation
- `DELETE /api/donations/{id}` - Delete donation

## Prerequisites

- **Python 3.11** - [Download](https://www.python.org/downloads/)
- **Azure Functions Core Tools v4** - [Install Guide](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- **Azure CLI** - [Install Guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Azure Subscription** - [Create Free Account](https://azure.microsoft.com/free/)

## Local Development Setup

### 1. Create virtual environment:
```bash
python -m venv venv
```

### 2. Activate virtual environment:
- **Windows:** `venv\Scripts\activate`
- **macOS/Linux:** `source venv/bin/activate`

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run locally with Azure Functions Core Tools:
```bash
func start
```

The API will be available at `http://localhost:7071`

### 5. Alternative - Run with Uvicorn (for development only):
```bash
uvicorn function_app:app --reload --port 8000
```

## API Documentation

When running locally:
- **Swagger UI:** `http://localhost:7071/docs`
- **ReDoc:** `http://localhost:7071/redoc`
- **Health Check:** `http://localhost:7071/api/health`

When deployed to Azure:
- **Swagger UI:** `https://your-function-app.azurewebsites.net/docs`
- **ReDoc:** `https://your-function-app.azurewebsites.net/redoc`
- **Health Check:** `https://your-function-app.azurewebsites.net/api/health`

## Azure Deployment

### Option 1: Automated Deployment (Recommended)

#### Using PowerShell (Windows):
```powershell
.\deploy.ps1
```

#### Using Bash (macOS/Linux):
```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
1. Create a resource group
2. Create a storage account
3. Create the Function App with Python 3.11 runtime
4. Configure CORS
5. Deploy your code

### Option 2: Manual Deployment

#### Step 1: Login to Azure
```bash
az login
```

#### Step 2: Create Resource Group
```bash
az group create --name church-app-rg --location eastus
```

#### Step 3: Create Storage Account
```bash
az storage account create \
  --name churchappstorage \
  --location eastus \
  --resource-group church-app-rg \
  --sku Standard_LRS
```

#### Step 4: Create Function App
```bash
az functionapp create \
  --resource-group church-app-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name church-management-api \
  --storage-account churchappstorage \
  --os-type Linux
```

#### Step 5: Configure CORS
```bash
az functionapp cors add \
  --name church-management-api \
  --resource-group church-app-rg \
  --allowed-origins "*"
```

#### Step 6: Deploy Code
```bash
func azure functionapp publish church-management-api --python
```

### Option 3: CI/CD with GitHub Actions

1. Copy `.github/workflows/azure-functions-deploy.yml` to your repository
2. Update `AZURE_FUNCTIONAPP_NAME` in the workflow file
3. Get your Function App publish profile:
   ```bash
   az functionapp deployment list-publishing-profiles \
     --name church-management-api \
     --resource-group church-app-rg \
     --xml
   ```
4. Add the publish profile as a GitHub secret named `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
5. Push to main branch to trigger deployment

### Option 4: CI/CD with Azure DevOps

1. Use the provided `azure-pipelines.yml` file
2. Update the variables:
   - `azureFunctionAppName`
   - `azureSubscription`
3. Create a pipeline in Azure DevOps
4. Run the pipeline

## Configuration

### Environment Variables

Configure these in Azure Portal under Function App → Configuration → Application Settings:

```
FUNCTIONS_WORKER_RUNTIME=python
PYTHON_ISOLATE_WORKER_DEPENDENCIES=1
CORS_ORIGINS=https://your-frontend-domain.com
DATABASE_PATH=/home/site/wwwroot/database
BLOB_PATH=/home/site/wwwroot/blob
```

### Local Settings

Edit `local.settings.json` for local development:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "CORS_ORIGINS": "*"
  }
}
```

## Azure Functions Architecture

### Key Files

- **`function_app.py`** - Main Azure Function entry point with FastAPI integration
- **`host.json`** - Function App host configuration
- **`local.settings.json`** - Local development settings (not deployed)
- **`requirements.txt`** - Python dependencies
- **`.funcignore`** - Files to exclude from deployment
- **`.python-version`** - Python version specification

### How It Works

1. Azure Functions receives HTTP requests
2. Requests are routed through `AsgiMiddleware` to FastAPI
3. FastAPI handles routing, validation, and business logic
4. Responses are returned through Azure Functions

### Benefits of Azure Functions

- **Serverless** - No server management required
- **Auto-scaling** - Scales automatically based on demand
- **Cost-effective** - Pay only for execution time
- **Built-in monitoring** - Application Insights integration
- **High availability** - Built-in redundancy
- **Easy deployment** - Multiple deployment options

## Monitoring and Logging

### View Logs in Azure Portal
1. Go to your Function App
2. Navigate to "Log stream" or "Application Insights"
3. View real-time logs and metrics

### View Logs Locally
```bash
func start --verbose
```

### Application Insights

Enable Application Insights for advanced monitoring:
```bash
az monitor app-insights component create \
  --app church-app-insights \
  --location eastus \
  --resource-group church-app-rg

az functionapp config appsettings set \
  --name church-management-api \
  --resource-group church-app-rg \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY=<your-key>
```

## Performance Optimization

### Cold Start Mitigation
- Use Premium Plan for production (eliminates cold starts)
- Enable "Always On" setting
- Use Application Insights for monitoring

### Scaling Configuration
Configure in `host.json`:
```json
{
  "http": {
    "maxOutstandingRequests": 200,
    "maxConcurrentRequests": 100
  }
}
```

## Troubleshooting

### Function not responding
1. Check logs in Azure Portal
2. Verify all dependencies are in `requirements.txt`
3. Ensure Python 3.11 is specified
4. Check Application Insights for errors

### CORS issues
```bash
az functionapp cors add \
  --name your-function-app \
  --resource-group your-rg \
  --allowed-origins "https://your-frontend.com"
```

### Deployment fails
1. Ensure Azure Functions Core Tools v4 is installed
2. Check `func --version` (should be 4.x)
3. Verify Python version: `python --version` (should be 3.11.x)
4. Clear local cache: `func extensions sync`

## Testing

### Local Testing
```bash
# Start the function
func start

# Test health endpoint
curl http://localhost:7071/api/health

# Test authentication
curl -X POST http://localhost:7071/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

### Production Testing
```bash
# Replace with your function app name
FUNCTION_URL="https://your-function-app.azurewebsites.net"

# Test health endpoint
curl $FUNCTION_URL/api/health

# View API documentation
open $FUNCTION_URL/docs
```

## Features

- **Clean Architecture:** Proper separation of concerns
- **Type Safety:** Full Pydantic validation
- **Error Handling:** Standardized error responses
- **Documentation:** Auto-generated API docs
- **CORS Support:** Frontend integration ready
- **Extensible:** Easy to add new features
- **Testable:** Each layer can be tested independently

## Default Admin Credentials

- **Username:** admin
- **Password:** password123

## Database Migration

The current implementation uses JSON files for data storage. When ready to migrate to PostgreSQL:

1. The repository layer abstracts database operations
2. Only the `base_repository.py` needs to be updated
3. All business logic remains unchanged
4. See `database/schema.md` for PostgreSQL schema

## Development Guidelines

1. **Controllers** should only handle HTTP concerns
2. **Services** contain all business logic
3. **Repositories** handle data persistence
4. **Models** define data structures
5. **Utils** provide reusable functionality

This structure ensures maintainability, testability, and scalability.
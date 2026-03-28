# Changelog

All notable changes to the Church Management System Backend will be documented in this file.

## [2.1.0] - Cloudflare R2 Storage Integration - 2026-02-08

### Added
- ☁️ **Cloudflare R2 Storage** - Migrated from local blob storage to Cloudflare R2
- 📦 **R2 Storage Service** (`app/services/r2_storage_service.py`)
  - Upload images to R2 with organized folder structure
  - Delete images from R2
  - S3-compatible API using boto3
  - Public read access for all images
- 🧪 **Testing & Migration Scripts**
  - `test_r2_connection.py` - Verify R2 connectivity and upload/delete operations
  - `migrate_urls_to_r2.py` - Convert database URLs from local paths to R2 URLs
  - `upload_existing_to_r2.py` - Upload existing blob images to R2
- 📚 **Comprehensive Documentation**
  - `R2_QUICKSTART.md` - Quick setup guide (5 minutes)
  - `R2_MIGRATION_GUIDE.md` - Detailed migration guide
  - `FRONTEND_R2_INTEGRATION.md` - Frontend integration guide
  - `R2_IMPLEMENTATION_SUMMARY.md` - Complete implementation summary
- 🔧 **Configuration**
  - R2 credentials in `app/config.py`
  - Environment variables for R2 (account ID, access keys, bucket name)
  - Updated `.env.example` with R2 configuration

### Changed
- 🔄 **Upload Controller** (`app/controllers/upload_controller.py`)
  - All endpoints now upload to R2 instead of local filesystem
  - Returns full R2 URLs instead of relative paths
  - Images only (videos not supported on R2)
- 🎠 **Carousel Service** (`app/services/carousel_service.py`)
  - Updated `upload_media_file()` to use R2
  - Organized carousel images by carousel name in R2
- 🚀 **Application Entry Points**
  - `main.py` - Removed static blob file mounting
  - `function_app.py` - Removed static blob file mounting
  - Images now served directly from R2 (no backend proxy)
- 📦 **Dependencies**
  - Added `boto3==1.34.34` for S3-compatible R2 access

### Removed
- 🗑️ **Static File Serving** - No longer serving blob files through backend
- 🗑️ **Local File Storage** - Images no longer stored in local `blob/` directory

### Migration Notes
- **Backend**: Install boto3, configure R2 credentials, test connection
- **Database**: Run `migrate_urls_to_r2.py` to update all JSON files
- **Frontend**: Update to use full R2 URLs instead of relative paths (see `FRONTEND_R2_INTEGRATION.md`)
- **Images**: Upload existing images to R2 using `upload_existing_to_r2.py`

### R2 Folder Structure
```
csi-ascit/
├── images/          # General images
├── logos/           # Church and diocese logos
├── priests/         # Priest photos
├── carousels/       # Carousel images (organized by carousel name)
└── ministries/      # Ministry images
```

### API Response Changes
- Upload endpoints now return `file_url` (full R2 URL) instead of `file_path` (relative path)
- Example: `https://c21ee9d90c8221d1f444e2d7723e6587.r2.cloudflarestorage.com/csi-ascit/images/abc123.jpg`

## [2.0.0] - Azure Functions Migration - 2024

### Added
- ✨ **Azure Functions Support** - Full migration to Azure Functions with Python 3.11
- 📦 **function_app.py** - Main Azure Function entry point with FastAPI integration
- ⚙️ **host.json** - Azure Functions host configuration
- 🔧 **local.settings.json** - Local development settings
- 📝 **.funcignore** - Deployment exclusion rules
- 🐍 **.python-version** - Python version specification (3.11)
- 🚀 **Deployment Scripts**
  - `deploy.ps1` - PowerShell deployment script for Windows
  - `deploy.sh` - Bash deployment script for macOS/Linux
- 🔄 **CI/CD Pipelines**
  - `.github/workflows/azure-functions-deploy.yml` - GitHub Actions workflow
  - `azure-pipelines.yml` - Azure DevOps pipeline
- 📚 **Documentation**
  - `DEPLOYMENT.md` - Comprehensive deployment guide
  - `QUICKSTART.md` - Quick start guide
  - `CHANGELOG.md` - This file
- 🧪 **Testing Scripts**
  - `test_local.ps1` - PowerShell local testing script
  - `test_deployment.py` - Python deployment testing script
- ⚙️ **Configuration**
  - `app/config.py` - Centralized configuration management
  - `.env.example` - Environment variables template
- 🔒 **Security**
  - `.gitignore` - Git exclusion rules
  - Environment-based configuration
  - Secure secrets management

### Changed
- 🔄 **Updated requirements.txt** - Added Azure Functions dependencies
  - `azure-functions==1.20.0`
  - `fastapi==0.109.2`
  - `pydantic==2.6.1`
  - Updated all dependencies to latest compatible versions
- 🌐 **Enhanced CORS** - Configurable CORS origins via environment variables
- 📊 **Improved Logging** - Better logging with Azure Functions integration
- 🏥 **Enhanced Health Check** - Added platform and environment detection
- 📖 **Updated README.md** - Complete Azure Functions documentation

### Improved
- ⚡ **Performance** - Optimized for Azure Functions serverless architecture
- 🔐 **Security** - Environment-based configuration for sensitive data
- 📈 **Scalability** - Auto-scaling with Azure Functions
- 🔍 **Monitoring** - Application Insights integration ready
- 🚀 **Deployment** - Multiple deployment options (manual, automated, CI/CD)

### Technical Details
- **Runtime:** Python 3.11
- **Platform:** Azure Functions v4
- **Framework:** FastAPI with ASGI middleware
- **Architecture:** Serverless
- **Deployment:** Consumption Plan (scalable to Premium)

### Migration Notes
- All existing FastAPI routes remain unchanged
- Controllers, services, and repositories work without modification
- JSON database files continue to work as-is
- Blob storage paths configurable via environment variables
- Backward compatible with existing frontend

### Breaking Changes
- None - Fully backward compatible with existing API clients

### Deployment Options
1. **Automated Scripts** - One-command deployment
2. **Manual Azure CLI** - Step-by-step deployment
3. **GitHub Actions** - Automated CI/CD
4. **Azure DevOps** - Enterprise CI/CD pipeline

### Configuration Changes
- CORS origins now configurable via `CORS_ORIGINS` environment variable
- Database path configurable via `DATABASE_PATH` environment variable
- Blob path configurable via `BLOB_PATH` environment variable
- All secrets should be set via Azure Function App settings

### Testing
- Local testing with Azure Functions Core Tools
- Automated testing scripts for both local and deployed functions
- Health check endpoint for monitoring

### Documentation
- Complete deployment guide with troubleshooting
- Quick start guide for rapid deployment
- CI/CD setup instructions
- Configuration examples
- Testing procedures

## [1.0.0] - Initial Release

### Added
- FastAPI backend with clean architecture
- Controllers for all major features
- Services layer for business logic
- Repositories for data access
- Pydantic models for validation
- Authentication system
- Member management
- Event management
- Ministry management
- Donation tracking
- Church home page management
- Carousel management
- File upload handling
- JSON-based data storage

### Features
- RESTful API design
- Auto-generated API documentation (Swagger/ReDoc)
- CORS support
- Input validation
- Error handling
- Standardized responses

---

## Version History

- **2.0.0** - Azure Functions Migration (Current)
- **1.0.0** - Initial FastAPI Implementation

## Upgrade Guide

### From 1.0.0 to 2.0.0

No code changes required! The migration to Azure Functions is transparent:

1. Install Azure Functions Core Tools v4
2. Install Azure CLI
3. Run deployment script
4. Update frontend API URL to Azure Functions URL

All existing API endpoints remain the same.

## Future Roadmap

### Version 2.1.0 (Planned)
- [ ] Azure SQL Database integration
- [ ] Azure Blob Storage for file uploads
- [ ] Azure Key Vault for secrets
- [ ] Enhanced authentication with Azure AD
- [ ] Rate limiting
- [ ] API versioning

### Version 2.2.0 (Planned)
- [ ] Real-time notifications with SignalR
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Advanced analytics
- [ ] Export functionality
- [ ] Backup and restore

### Version 3.0.0 (Future)
- [ ] Microservices architecture
- [ ] GraphQL API
- [ ] Mobile app backend
- [ ] Multi-tenant support
- [ ] Advanced reporting
- [ ] Integration with church management systems

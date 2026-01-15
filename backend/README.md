# Church App Backend

A clean, well-structured FastAPI backend following best practices with proper separation of concerns.

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

## Setup Instructions

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

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
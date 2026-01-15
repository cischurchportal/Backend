# Church Database Schema

This document describes the JSON database structure for the Church Application. These JSON files will be easily transferable to PostgreSQL later.

## Tables Overview

### 1. users.json
Admin and system users for the application.

**Fields:**
- `id` (int): Primary key
- `username` (string): Unique username
- `password` (string): Password (will be hashed in production)
- `email` (string): User email
- `role` (string): User role (admin, staff, etc.)
- `first_name` (string): First name
- `last_name` (string): Last name
- `created_at` (datetime): Account creation timestamp
- `last_login` (datetime): Last login timestamp
- `is_active` (boolean): Account status

### 2. members.json
Church members information.

**Fields:**
- `id` (int): Primary key
- `first_name` (string): Member's first name
- `last_name` (string): Member's last name
- `email` (string): Contact email
- `phone` (string): Phone number
- `address` (string): Home address
- `date_of_birth` (date): Birth date
- `membership_date` (date): Date joined church
- `membership_status` (string): active, inactive, transferred
- `ministry_involvement` (array): List of ministry IDs
- `emergency_contact` (object): Emergency contact information
- `created_at` (datetime): Record creation timestamp
- `updated_at` (datetime): Last update timestamp

### 3. events.json
Church events and services.

**Fields:**
- `id` (int): Primary key
- `title` (string): Event name
- `description` (text): Event description
- `event_type` (string): worship, bible_study, youth, etc.
- `start_datetime` (datetime): Event start time
- `end_datetime` (datetime): Event end time
- `location` (string): Event location
- `is_recurring` (boolean): Whether event repeats
- `recurrence_pattern` (string): weekly, monthly, etc.
- `max_attendees` (int): Maximum capacity
- `current_attendees` (int): Current registration count
- `registration_required` (boolean): Whether registration is needed
- `created_by` (int): User ID who created event
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### 4. ministries.json
Church ministries and groups.

**Fields:**
- `id` (int): Primary key
- `name` (string): Ministry name
- `description` (text): Ministry description
- `leader_id` (int): Member ID of ministry leader
- `meeting_schedule` (string): When ministry meets
- `location` (string): Where ministry meets
- `contact_email` (string): Contact email
- `members` (array): Array of member IDs
- `requirements` (string): Membership requirements
- `is_active` (boolean): Ministry status
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### 5. donations.json
Financial contributions tracking.

**Fields:**
- `id` (int): Primary key
- `member_id` (int): Member ID (null for anonymous)
- `amount` (decimal): Donation amount
- `donation_type` (string): tithe, offering, special
- `payment_method` (string): cash, check, online
- `check_number` (string): Check number if applicable
- `donation_date` (date): Date of donation
- `fund` (string): general, missions, building, etc.
- `notes` (text): Additional notes
- `is_anonymous` (boolean): Anonymous donation flag
- `tax_deductible` (boolean): Tax deductible status
- `created_at` (datetime): Record creation timestamp

### 6. attendance.json
Event attendance tracking.

**Fields:**
- `id` (int): Primary key
- `event_id` (int): Event ID
- `member_id` (int): Member ID
- `attendance_date` (date): Date of attendance
- `status` (string): present, absent, late
- `check_in_time` (datetime): When member checked in
- `notes` (text): Additional notes
- `created_at` (datetime): Record creation timestamp

## Relationships

- `users.id` → `events.created_by`
- `members.id` → `ministries.leader_id`
- `members.id` → `ministries.members[]`
- `members.id` → `donations.member_id`
- `events.id` → `attendance.event_id`
- `members.id` → `attendance.member_id`

## PostgreSQL Migration Notes

When migrating to PostgreSQL:

1. **Data Types**: Convert datetime strings to TIMESTAMP WITH TIME ZONE
2. **Arrays**: Convert JSON arrays to PostgreSQL arrays or separate junction tables
3. **Objects**: Convert nested objects to separate tables or JSONB columns
4. **Constraints**: Add proper foreign key constraints
5. **Indexes**: Add indexes on frequently queried fields
6. **Security**: Hash passwords using bcrypt or similar

## Sample PostgreSQL Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(20) DEFAULT 'member',
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true
);

-- Members table
CREATE TABLE members (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    address TEXT,
    date_of_birth DATE,
    membership_date DATE,
    membership_status VARCHAR(20) DEFAULT 'active',
    emergency_contact JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- And so on for other tables...
```
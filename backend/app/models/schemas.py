from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Auth schemas
class LoginCredentials(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    success: bool
    user: Optional[dict] = None

# User schemas
class UserBase(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = "member"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: str
    last_login: Optional[str] = None

# Member schemas
class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[str] = None
    membership_status: str = "active"

class MemberCreate(MemberBase):
    membership_date: Optional[str] = None
    ministry_involvement: List[str] = []
    emergency_contact: Optional[dict] = None

class MemberResponse(MemberBase):
    id: int
    membership_date: Optional[str] = None
    ministry_involvement: List[str] = []
    emergency_contact: Optional[dict] = None
    created_at: str
    updated_at: str

# Event schemas
class EventBase(BaseModel):
    title: str
    description: str
    event_type: str
    start_datetime: str
    end_datetime: str
    location: str
    is_recurring: bool = False
    recurrence_pattern: Optional[str] = None
    max_attendees: Optional[int] = None
    registration_required: bool = False

class EventCreate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    current_attendees: int = 0
    created_by: int
    created_at: str
    updated_at: str

# Ministry schemas
class MinistryBase(BaseModel):
    name: str
    description: str
    meeting_schedule: str
    location: str
    contact_email: str
    requirements: Optional[str] = None
    is_active: bool = True

class MinistryCreate(MinistryBase):
    leader_id: int

class MinistryResponse(MinistryBase):
    id: int
    leader_id: int
    members: List[int] = []
    created_at: str
    updated_at: str

# Donation schemas
class DonationBase(BaseModel):
    amount: float
    donation_type: str
    payment_method: str
    donation_date: str
    fund: str = "general"
    notes: Optional[str] = None
    is_anonymous: bool = False
    tax_deductible: bool = True

class DonationCreate(DonationBase):
    member_id: Optional[int] = None
    check_number: Optional[str] = None

class DonationResponse(DonationBase):
    id: int
    member_id: Optional[int] = None
    check_number: Optional[str] = None
    created_at: str
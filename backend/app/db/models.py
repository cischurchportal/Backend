"""
SQLAlchemy ORM models for Azure SQL Database.
Tables are auto-created/altered via create_all with checkfirst=True.
"""
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime,
    Date, ForeignKey, JSON
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(20), default="member")
    first_name = Column(String(100))
    last_name = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=True)
    phone = Column(String(30), nullable=True)
    address = Column(Text, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    membership_date = Column(Date, nullable=True)
    membership_status = Column(String(20), default="active")
    # Stored as JSON array of ministry names
    ministry_involvement = Column(JSON, default=list)
    # Stored as JSON object
    emergency_contact = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    event_type = Column(String(50))
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)
    location = Column(String(255))
    is_recurring = Column(Boolean, default=False)
    recurrence_pattern = Column(String(50), nullable=True)
    max_attendees = Column(Integer, nullable=True)
    current_attendees = Column(Integer, default=0)
    registration_required = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Ministry(Base):
    __tablename__ = "ministries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    time = Column(String(100), nullable=True)
    image = Column(String(500), nullable=True)
    contact_phone = Column(String(30), nullable=True)
    leader_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    meeting_schedule = Column(String(255))
    location = Column(String(255))
    contact_email = Column(String(255))
    # Stored as JSON array of member IDs
    members = Column(JSON, default=list)
    requirements = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Donation(Base):
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    amount = Column(Float, nullable=False)
    donation_type = Column(String(50))
    payment_method = Column(String(50))
    check_number = Column(String(50), nullable=True)
    donation_date = Column(String(50))
    fund = Column(String(50), default="general")
    notes = Column(Text, nullable=True)
    is_anonymous = Column(Boolean, default=False)
    tax_deductible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChurchSettings(Base):
    __tablename__ = "church_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    church_name = Column(String(255))
    diocese_logo = Column(String(500), nullable=True)
    church_logo = Column(String(500), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)
    established_year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Priest(Base):
    __tablename__ = "priests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    title = Column(String(100))
    image = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    ordination_year = Column(Integer, nullable=True)
    # Stored as JSON array of strings
    specializations = Column(JSON, default=list)
    contact_email = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VerseOfDay(Base):
    __tablename__ = "verse_of_day"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(10))
    verse = Column(Text)
    reference = Column(String(100))
    commentary = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text)
    type = Column(String(50), default="general")
    priority = Column(String(20), default="medium")
    start_date = Column(String(10), nullable=True)
    end_date = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ServiceTiming(Base):
    __tablename__ = "service_timings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(255), nullable=False)
    day_of_week = Column(String(20))
    time = Column(String(10))
    duration_minutes = Column(Integer, nullable=True)
    preacher = Column(String(255), nullable=True)
    service_type = Column(String(50))
    language = Column(String(50), default="English")
    location = Column(String(255))
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Celebration(Base):
    __tablename__ = "celebrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=True)
    celebration_type = Column(String(50))
    date = Column(String(10))
    member_name = Column(String(255))
    age = Column(Integer, nullable=True)
    years_married = Column(Integer, nullable=True)
    message = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Carousel(Base):
    __tablename__ = "carousels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(50), default="general")
    is_active = Column(Boolean, default=True)
    display_order = Column(Integer, default=1)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    media = relationship("CarouselMedia", back_populates="carousel", cascade="all, delete-orphan")


class CarouselMedia(Base):
    __tablename__ = "carousel_media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    carousel_id = Column(Integer, ForeignKey("carousels.id"), nullable=False)
    media_type = Column(String(20))
    file_path = Column(String(500))
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    display_order = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    carousel = relationship("Carousel", back_populates="media")


class AboutPage(Base):
    __tablename__ = "about_page"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    history = Column(Text, nullable=True)
    # Stored as JSON array of image URLs
    images = Column(JSON, default=list)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Developer(Base):
    __tablename__ = "developers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    role = Column(String(100))
    image = Column(String(500), nullable=True)
    order = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

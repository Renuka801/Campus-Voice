import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator
from app.models import IssueCategory, ComplaintStatus
import os


class StudentCreate(BaseModel):
    full_name: str
    email: EmailStr
    roll_number: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_college_email(cls, v):
        domain = os.getenv("ALLOWED_EMAIL_DOMAIN", "")
        if domain and not v.lower().endswith("@" + domain.lower()):
            raise ValueError(f"Only @{domain} college email addresses are allowed")
        return v


class StudentLogin(BaseModel):
    email: EmailStr
    password: str


class StudentOut(BaseModel):
    id: uuid.UUID
    full_name: str
    email: EmailStr
    roll_number: str
    is_admin: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ComplaintCreate(BaseModel):
    category: IssueCategory
    title: str
    description: str
    is_anonymous: bool = False


class ComplaintOut(BaseModel):
    id: uuid.UUID
    tracking_id: uuid.UUID
    is_anonymous: bool
    category: IssueCategory
    title: str
    description: str
    status: ComplaintStatus
    admin_remarks: Optional[str] = None
    created_at: datetime
    student_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True


class ComplaintStatusUpdate(BaseModel):
    status: ComplaintStatus
    admin_remarks: Optional[str] = None


class TrackingLookup(BaseModel):
    tracking_id: uuid.UUID

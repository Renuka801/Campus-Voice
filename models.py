import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class IssueCategory(str, enum.Enum):
    water = "Water Problem"
    hostel = "Hostel Problem"
    lecturer = "Lecturer Problem"
    student_related = "Student Related"
    infrastructure = "Infrastructure"
    academic = "Academic Issues"
    transportation = "Transportation"
    safety = "Safety"
    other = "Other"


class ComplaintStatus(str, enum.Enum):
    pending = "Pending"
    in_progress = "In Progress"
    resolved = "Resolved"
    rejected = "Rejected"


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    roll_number = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    complaints = relationship("Complaint", back_populates="student")


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tracking_id = Column(UUID(as_uuid=True), unique=True, default=uuid.uuid4, index=True)

    # NULL when the complaint is anonymous — identity is not recoverable
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=True)

    is_anonymous = Column(Boolean, default=False)
    category = Column(Enum(IssueCategory), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum(ComplaintStatus), default=ComplaintStatus.pending)
    admin_remarks = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = relationship("Student", back_populates="complaints")

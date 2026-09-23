from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.post("/", response_model=schemas.ComplaintOut)
def create_complaint(
    complaint: schemas.ComplaintCreate,
    db: Session = Depends(get_db),
    current_student=Depends(auth.get_current_student),
):
    new_complaint = models.Complaint(
        student_id=None if complaint.is_anonymous else current_student.id,
        is_anonymous=complaint.is_anonymous,
        category=complaint.category,
        title=complaint.title,
        description=complaint.description,
    )
    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    return new_complaint


@router.get("/my", response_model=List[schemas.ComplaintOut])
def get_my_complaints(
    db: Session = Depends(get_db),
    current_student=Depends(auth.get_current_student),
):
    # Only returns non-anonymous complaints tied to this student.
    # Anonymous ones aren't linked to any student_id, so they can't be listed here —
    # that's intentional, use tracking_id lookup instead.
    return db.query(models.Complaint).filter(models.Complaint.student_id == current_student.id).all()


@router.post("/track", response_model=schemas.ComplaintOut)
def track_complaint(lookup: schemas.TrackingLookup, db: Session = Depends(get_db)):
    complaint = db.query(models.Complaint).filter(models.Complaint.tracking_id == lookup.tracking_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="No complaint found with that tracking ID")
    return complaint


@router.get("/", response_model=List[schemas.ComplaintOut])
def get_all_complaints(
    category: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db),
    current_admin=Depends(auth.get_current_admin),
):
    query = db.query(models.Complaint)
    if category:
        query = query.filter(models.Complaint.category == category)
    if status_filter:
        query = query.filter(models.Complaint.status == status_filter)
    return query.order_by(models.Complaint.created_at.desc()).all()


@router.patch("/{complaint_id}", response_model=schemas.ComplaintOut)
def update_complaint_status(
    complaint_id: str,
    update: schemas.ComplaintStatusUpdate,
    db: Session = Depends(get_db),
    current_admin=Depends(auth.get_current_admin),
):
    complaint = db.query(models.Complaint).filter(models.Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    complaint.status = update.status
    if update.admin_remarks is not None:
        complaint.admin_remarks = update.admin_remarks
    db.commit()
    db.refresh(complaint)
    return complaint

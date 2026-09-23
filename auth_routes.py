from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.StudentOut)
def register(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    existing_email = db.query(models.Student).filter(models.Student.email == student.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_roll = db.query(models.Student).filter(models.Student.roll_number == student.roll_number).first()
    if existing_roll:
        raise HTTPException(status_code=400, detail="Roll number already registered")

    new_student = models.Student(
        full_name=student.full_name,
        email=student.email,
        roll_number=student.roll_number,
        hashed_password=auth.hash_password(student.password),
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.email == form_data.username).first()
    if not student or not auth.verify_password(form_data.password, student.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = auth.create_access_token(data={"sub": str(student.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.StudentOut)
def get_me(current_student=Depends(auth.get_current_student)):
    return current_student

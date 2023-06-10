from fastapi import APIRouter, Depends, status, HTTPException
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas

router = APIRouter()


@router.post(
    "/student",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Student,
)
def create_student(
    student_data: schemas.CreateStudentSchema, db: Session = Depends(get_db)
):
    visitor = (
        db.query(models.UnivercityVisitor)
        .filter(
            models.UnivercityVisitor.passport_id
            == str(student_data.passport_id.lower())
        )
        .first()
    )
    if visitor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same passport id already exist",
        )
    new_visitor = models.UnivercityVisitor(
        name=student_data.name,
        middle_name=student_data.middle_name,
        last_name=student_data.last_name,
        birthdate=student_data.birthdate,
        passport_id=student_data.passport_id,
    )
    db.add(new_visitor)
    db.flush()
    new_student_group = db.query(models.Group).get(student_data.group_id)
    if not new_student_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Group with id {student_data.group_id} not found!",
        )
    new_student = models.Student(
        visitor_id=new_visitor.id, group_id=int(student_data.group_id)
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    response = schemas.Student(
        id=new_student.id,
        name=new_visitor.name,
        middle_name=new_visitor.middle_name,
        last_name=new_visitor.last_name,
        passport_id=new_visitor.passport_id,
        birthdate=new_visitor.birthdate,
        group=new_student.group.name,
    )
    db.close()
    return response


@router.get(
    "/student",
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = (
        db.query(models.Student)
        .filter(models.Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.close()
    return student

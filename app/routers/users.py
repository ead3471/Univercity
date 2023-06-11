from fastapi import APIRouter, Depends, status, HTTPException

from ..models.users import Student, Teacher, UnivercityVisitor
from ..models.education import Course
from ..models.structure import Group
from ..database import get_db
from sqlalchemy.orm import Session
from .. import schemas

router = APIRouter()


@router.post(
    "/student",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Student,
    description="Create student with specified data",
)
def create_student(
    student_data: schemas.CreateStudentSchema, db: Session = Depends(get_db)
):
    visitor = (
        db.query(UnivercityVisitor)
        .filter(
            UnivercityVisitor.passport_id
            == str(student_data.passport_id.lower())
        )
        .first()
    )
    if visitor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same passport id already exist",
        )
    new_visitor = UnivercityVisitor(
        name=student_data.name,
        middle_name=student_data.middle_name,
        last_name=student_data.last_name,
        birthdate=student_data.birthdate,
        passport_id=student_data.passport_id,
    )
    db.add(new_visitor)
    db.flush()
    new_student_group = db.query(Group).get(student_data.group_id)
    if not new_student_group:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Group with id {student_data.group_id} not found!",
        )
    new_student = Student(
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
    "/student/{student_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Student,
    description="Return data of specifed student",
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student: Student = (
        db.query(Student).filter(Student.id == student_id).first()
    )

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    response = schemas.Student(
        id=student.id,
        name=student.visitor.name,
        middle_name=student.visitor.middle_name,
        last_name=student.visitor.last_name,
        passport_id=student.visitor.passport_id,
        birthdate=student.visitor.birthdate,
        group=student.group.name if student.group else None,
    )
    db.close()
    return response


@router.patch(
    "/student/{student_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Student,
    description="Patch student with specified data",
)
def patch_student(
    student_id: int,
    student_data: schemas.CreateStudentSchema,
    db: Session = Depends(get_db),
):
    student: Student = db.query(Student).get(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if "group" in student_data:
        group = db.query(Group).get(student_data.group_id)
        if group:
            student.group = group

    def set_attr_if_not_None(obj, attr, value):
        if value:
            setattr(obj, attr, value)

    visitor: UnivercityVisitor = student.visitor

    for key, value in student_data:
        if hasattr(visitor, key) and value:
            setattr(visitor, key, value)

    response = schemas.Student(
        id=student.id,
        name=student.visitor.name,
        middle_name=student.visitor.middle_name,
        last_name=student.visitor.last_name,
        passport_id=student.visitor.passport_id,
        birthdate=student.visitor.birthdate,
        group=student.group.name if student.group else None,
    )
    db.commit()
    db.close()
    return response


@router.delete(
    "/student/{student_id:int}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete the specifed student",
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student: Student = (
        db.query(Student).filter(Student.id == student_id).first()
    )

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

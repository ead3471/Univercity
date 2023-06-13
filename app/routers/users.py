from fastapi import APIRouter, Depends, status, HTTPException

from ..models.users import Student, Teacher, UnivercityVisitor
from ..models.education import Course
from ..models.structure import Group
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas.users_schemas import (
    CreateStudentSchema,
    CreateTeacherSchema,
    GetStudentSchema,
    GetTeacherSchema,
    UpdateStudentSchema,
    UpdateTeacherSchema,
    GetVisitorSchema,
)

router = APIRouter()


@router.post("/students", response_model=GetStudentSchema, status_code=201)
def create_student(
    student_data: CreateStudentSchema, db: Session = Depends(get_db)
):
    if (
        db.query(Student)
        .filter_by(passport_id=student_data.passport_id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same passport ID already exists",
        )

    if student_data.group_id is not None:
        if db.query(Group).get(student_data.group_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="specified group does not exists",
            )

    new_student = Student(**student_data.dict())

    db.add(new_student)
    db.commit()
    response = GetStudentSchema.from_orm(new_student)
    db.close()

    return response


@router.get(
    "/students/{student_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetStudentSchema,
    description="Return data of specifed student",
)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student: Student = db.query(Student).get(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    response = GetStudentSchema.from_orm(student)
    db.close()
    return response


@router.patch(
    "/students/{student_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetStudentSchema,
    description="Patch student with specified data",
)
def patch_student(
    student_id: int,
    student_data: UpdateStudentSchema,
    db: Session = Depends(get_db),
):
    student: Student = db.query(Student).get(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student_data:
        if hasattr(student, key) and value:
            setattr(student, key, value)

    db.commit()
    response = GetStudentSchema.from_orm(student)
    db.close()
    return response


@router.delete(
    "/students/{student_id:int}",
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


@router.post(
    "/teachers",
    status_code=status.HTTP_201_CREATED,
    response_model=GetTeacherSchema,
    description="Create teacher with specified data",
)
def create_teacher(
    teacher_data: CreateTeacherSchema, db: Session = Depends(get_db)
):
    if (
        db.query(Teacher)
        .filter_by(passport_id=teacher_data.passport_id)
        .first()
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Teacher with same passport id already exist",
        )

    teacher_dict = teacher_data.dict()
    courses_ids: list = teacher_dict.pop("courses")

    if courses_ids is not None:
        courses = db.query(Course).filter(Course.id.in_(courses_ids)).all()
        if len(courses_ids) != len(courses):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="One of the given courses are not exists",
            )

        teacher_dict["courses"] = courses

    new_teacher = Teacher(**teacher_dict)

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    response = GetTeacherSchema.from_orm(new_teacher)
    db.close()
    return response


@router.get(
    "/teachers/{teacher_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetTeacherSchema,
    description="Return data of specifed teacher",
)
def get_teacher(teacher_id: int, db: Session = Depends(get_db)):
    teacher: Teacher = db.query(Teacher).get(teacher_id)

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    response = GetTeacherSchema.from_orm(teacher)
    db.close()
    return response


@router.patch(
    "/teachers/{teacher_id:int}",
    status_code=status.HTTP_200_OK,
    response_model=GetTeacherSchema,
    description="Patch teacher with specified data",
)
def patch_teacher(
    teacher_id: int,
    teacher_data: UpdateTeacherSchema,
    db: Session = Depends(get_db),
):
    teacher: Teacher = db.query(Teacher).get(teacher_id)

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    teacher_data_dict = teacher_data.dict()

    courses = teacher_data_dict.pop("courses")

    if courses is not None:
        teacher.courses.clear()
        new_courses = (
            db.query(Course).filter(Course.id.in_(teacher_data.courses)).all()
        )

        teacher.courses = new_courses

    for key, value in teacher_data_dict.items():
        if hasattr(teacher, key) and value:
            setattr(teacher, key, value)

    db.commit()
    response = GetTeacherSchema.from_orm(teacher)
    db.close()
    return response

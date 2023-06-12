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
    UpdateTeacherSchema,
    UpdateTeacherSchema,
)

router = APIRouter()


@router.post(
    "/students",
    status_code=status.HTTP_201_CREATED,
    response_model=GetStudentSchema,
    description="Create student with specified data",
)
def create_student(
    student_data: CreateStudentSchema, db: Session = Depends(get_db)
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
    student_data: UpdateTeacherSchema,
    db: Session = Depends(get_db),
):
    student: Student = db.query(Student).get(student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if "group" in student_data:
        group = db.query(Group).get(student_data.group_id)
        if group:
            student.group = group

    visitor: UnivercityVisitor = student.visitor

    for key, value in student_data:
        if hasattr(visitor, key) and value:
            setattr(visitor, key, value)

    response = GetStudentSchema(
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
    visitor = (
        db.query(UnivercityVisitor)
        .filter(
            UnivercityVisitor.passport_id
            == str(teacher_data.passport_id.lower())
        )
        .first()
    )
    if visitor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with same passport id already exist",
        )
    new_visitor = UnivercityVisitor(
        name=teacher_data.name,
        middle_name=teacher_data.middle_name,
        last_name=teacher_data.last_name,
        birthdate=teacher_data.birthdate,
        passport_id=teacher_data.passport_id,
    )
    db.add(new_visitor)
    db.flush()

    new_teacher = Teacher(visitor_id=new_visitor.id)
    if teacher_data.courses:
        new_teacher_courses = (
            db.query(Course).filter(Course.id.in_(teacher_data.courses)).all()
        )

        if len(new_teacher_courses) != len(teacher_data.courses):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "One or more course IDs are invalid.",
            )

        new_teacher.courses = new_teacher_courses

    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    response = GetTeacherSchema(
        id=new_teacher.id,
        name=new_visitor.name,
        middle_name=new_visitor.middle_name,
        last_name=new_visitor.last_name,
        passport_id=new_visitor.passport_id,
        birthdate=new_visitor.birthdate,
        courses=new_teacher.courses,
    )
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

    response = GetTeacherSchema(
        id=teacher.id,
        name=teacher.visitor.name,
        middle_name=teacher.visitor.middle_name,
        last_name=teacher.visitor.last_name,
        passport_id=teacher.visitor.passport_id,
        birthdate=teacher.visitor.birthdate,
        courses=teacher.courses,
    )
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

    print(teacher_data)

    if teacher_data.courses is not None:
        teacher.courses.clear()
        new_courses = (
            db.query(Course).filter(Course.id.in_(teacher_data.courses)).all()
        )

        teacher.courses = new_courses
        print(teacher.courses)

    visitor: UnivercityVisitor = teacher.visitor

    for key, value in teacher_data:
        if hasattr(visitor, key) and value:
            setattr(visitor, key, value)

    response = GetTeacherSchema(
        id=teacher.id,
        name=teacher.visitor.name,
        middle_name=teacher.visitor.middle_name,
        last_name=teacher.visitor.last_name,
        passport_id=teacher.visitor.passport_id,
        birthdate=teacher.visitor.birthdate,
    )
    db.commit()
    db.close()
    return response

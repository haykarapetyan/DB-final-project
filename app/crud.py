from sqlalchemy.orm import Session
from sqlalchemy import func, text, update
from typing import List, Optional

from . import models, schemas

# --- Generic CRUD Functions ---

def get_by_id(db: Session, model, id: int):
    return db.query(model).filter(model.id == id).first()

def get_all(db: Session, model, skip: int, limit: int):
    return db.query(model).offset(skip).limit(limit).all()

def create(db: Session, model, schema):
    db_obj = model(**schema.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# --- Specific Getters for Duplicate Checks ---

def get_faculty_by_name(db: Session, name: str):
    return db.query(models.Faculty).filter(models.Faculty.name == name).first()

def get_group_by_code(db: Session, code: str):
    return db.query(models.Group).filter(models.Group.code == code).first()

def get_department_by_name(db: Session, name: str):
    return db.query(models.Department).filter(models.Department.name == name).first()

def get_subject_by_name(db: Session, name: str):
    return db.query(models.Subject).filter(models.Subject.name == name).first()

def get_teacher_by_name(db: Session, name: str):
    return db.query(models.Teacher).filter(models.Teacher.name == name).first()


# --- Complex Queries ---

def search_groups(db: Session, faculty_id: Optional[int], min_students: int, sort_by: Optional[str], skip: int, limit: int):
    """ SELECT ... WHERE (с несколькими условиями) + sorting """
    query = db.query(models.Group)
    if faculty_id:
        query = query.filter(models.Group.faculty_id == faculty_id)
    if min_students > 0:
        query = query.filter(models.Group.num_students >= min_students)
    if sort_by and hasattr(models.Group, sort_by):
        query = query.order_by(getattr(models.Group, sort_by))
    return query.offset(skip).limit(limit).all()

def get_session_details(db: Session, skip: int, limit: int):
    """ JOIN example """
    return db.query(models.Session).offset(skip).limit(limit).all()

def promote_groups(db: Session, current_course: int):
    """ UPDATE с нетривиальным условием """
    stmt = (
        update(models.Group)
        .where(models.Group.course == current_course)
        .values(course=models.Group.course + 1)
    )
    result = db.execute(stmt)
    db.commit()
    return result.rowcount

def get_students_per_faculty(db: Session) -> List[schemas.FacultyStats]:
    """ GROUP BY example """
    result = (
        db.query(
            models.Faculty.name.label("faculty_name"),
            func.sum(models.Group.num_students).label("total_students")
        )
        .join(models.Group, models.Faculty.id == models.Group.faculty_id)
        .group_by(models.Faculty.name)
        .all()
    )
    return result

def search_subjects_by_trgm(db: Session, query: str):
    """ Full-text search using pg_trgm similarity """
    # Requires pg_trgm extension and a GIN/GIST index on the JSON field.
    return db.query(models.Subject).filter(text("extra->>'notes' % :query")).params(query=query).all()

def search_subjects_by_regex(db: Session, pattern: str):
    """ Search using PostgreSQL regex """
    return db.query(models.Subject).filter(text("extra->>'notes' ~ :pattern")).params(pattern=pattern).all()
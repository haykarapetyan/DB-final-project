from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import crud, models, schemas
from .database import get_db

app = FastAPI(
    title="University Session API",
    description="A refactored API for managing university entities, fulfilling all project requirements.",
    version="1.0.0",
)

# --- Routers ---
router = APIRouter()

# --- Root ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the University Session API. Visit /docs for documentation."}

# --- CRUD Endpoints ---

# Helper function to check for duplicates
def check_duplicate(db: Session, entity_name: str, field: str, value: str):
    getter = getattr(crud, f"get_{entity_name.lower()}_by_{field}")
    if getter(db, value):
        raise HTTPException(status_code=400, detail=f"{entity_name} with this {field} already exists.")

@router.post("/faculties/", response_model=schemas.Faculty, tags=["Faculties"])
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    check_duplicate(db, "Faculty", "name", faculty.name)
    return crud.create(db, models.Faculty, faculty)

@router.get("/faculties/", response_model=List[schemas.Faculty], tags=["Faculties"])
def read_faculties(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all(db, models.Faculty, skip, limit)

@router.post("/departments/", response_model=schemas.Department, tags=["Departments"])
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    check_duplicate(db, "Department", "name", department.name)
    return crud.create(db, models.Department, department)

@router.get("/departments/", response_model=List[schemas.Department], tags=["Departments"])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all(db, models.Department, skip, limit)

@router.post("/teachers/", response_model=schemas.Teacher, tags=["Teachers"])
def create_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(get_db)):
    # Assuming teacher names are not unique, so no duplicate check
    return crud.create(db, models.Teacher, teacher)

@router.get("/teachers/", response_model=List[schemas.Teacher], tags=["Teachers"])
def read_teachers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all(db, models.Teacher, skip, limit)

@router.post("/groups/", response_model=schemas.Group, tags=["Groups"])
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    check_duplicate(db, "Group", "code", group.code)
    if not crud.get_by_id(db, models.Faculty, group.faculty_id):
        raise HTTPException(status_code=404, detail="Faculty not found")
    return crud.create(db, models.Group, group)

@router.get("/groups/", response_model=List[schemas.Group], tags=["Groups"])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all(db, models.Group, skip, limit)

@router.post("/subjects/", response_model=schemas.Subject, tags=["Subjects"])
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    check_duplicate(db, "Subject", "name", subject.name)
    if not crud.get_by_id(db, models.Department, subject.department_id):
        raise HTTPException(status_code=404, detail="Department not found")
    return crud.create(db, models.Subject, subject)

@router.get("/subjects/", response_model=List[schemas.Subject], tags=["Subjects"])
def read_subjects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all(db, models.Subject, skip, limit)

@router.post("/sessions/", response_model=schemas.Session, tags=["Sessions"])
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db)):
    if not crud.get_by_id(db, models.Group, session.group_id):
        raise HTTPException(status_code=404, detail="Group not found")
    if not crud.get_by_id(db, models.Subject, session.subject_id):
        raise HTTPException(status_code=404, detail="Subject not found")
    if not crud.get_by_id(db, models.Teacher, session.teacher_id):
        raise HTTPException(status_code=404, detail="Teacher not found")
    return crud.create(db, models.Session, session)

@router.get("/sessions/", response_model=List[schemas.Session], tags=["Sessions"])
def read_sessions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all(db, models.Session, skip, limit)

# --- Complex Queries ---

@router.get("/groups/search/", response_model=List[schemas.Group], tags=["Groups"], summary="5a. Select with multiple WHERE and sorting")
def search_groups_endpoint(
    faculty_id: Optional[int] = None,
    min_students: int = Query(0, ge=0),
    sort_by: Optional[str] = Query(None, enum=["code", "course", "num_students"], description="Sort by 'code', 'course', or 'num_students'"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    **SELECT ... WHERE (with multiple conditions) + Sorting**
    - Filter groups by `faculty_id` and/or `min_students`.
    - Sort results by a given field.
    - Implements pagination with `skip` and `limit`.
    """
    return crud.search_groups(db, faculty_id, min_students, sort_by, skip, limit)

@router.get("/sessions/details/", response_model=List[schemas.SessionDetails], tags=["Sessions"], summary="5b. JOIN example")
def get_session_details_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    **JOIN**
    - Fetches session records and joins them with related Group, Subject, and Teacher data.
    - The relationships are handled by SQLAlchemy ORM and represented in the nested `SessionDetails` schema.
    - Implements pagination with `skip` and `limit`.
    """
    return crud.get_session_details(db, skip, limit)

@router.put("/groups/promote/", tags=["Groups"], summary="5c. UPDATE with non-trivial condition")
def promote_groups_endpoint(current_course: int, db: Session = Depends(get_db)):
    """
    **UPDATE with a non-trivial condition**
    - Finds all groups in a `current_course` and increments their course number by 1.
    - Returns the count of updated group records.
    """
    updated_count = crud.promote_groups(db, current_course)
    if updated_count == 0:
        raise HTTPException(status_code=404, detail=f"No groups found for course {current_course} to promote.")
    return {"message": f"Promoted {updated_count} groups from course {current_course}."}

@router.get("/reports/students-per-faculty/", response_model=List[schemas.FacultyStats], tags=["Reports"], summary="5d. GROUP BY example")
def get_students_per_faculty_endpoint(db: Session = Depends(get_db)):
    """
    **GROUP BY**
    - Calculates the total number of students for each faculty.
    - Uses `GROUP BY` on faculty name and `SUM` on the number of students.
    """
    return crud.get_students_per_faculty(db)

@router.get("/subjects/search-trgm/", response_model=List[schemas.Subject], tags=["Subjects"], summary="6a. Full-text search with pg_trgm")
def search_subjects_trgm_endpoint(query: str, db: Session = Depends(get_db)):
    """
    **Full-text search using pg_trgm similarity**
    - Searches for subjects where the `extra['notes']` field is similar to the query string.
    - Requires the `pg_trgm` extension and a GIN/GIST index on the JSON field for performance.
    """
    return crud.search_subjects_by_trgm(db, query)

@router.get("/subjects/search-regex/", response_model=List[schemas.Subject], tags=["Subjects"], summary="6b. Full-text search with Regex")
def search_subjects_regex_endpoint(pattern: str = Query(..., example="^Intro.*"), db: Session = Depends(get_db)):
    """
    **Full-text search using PostgreSQL regular expressions**
    - Searches for subjects where `extra['notes']` matches the given regex pattern (case-sensitive).
    - Example: `^Intro.*` finds notes starting with "Intro".
    """
    return crud.search_subjects_by_regex(db, pattern)

app.include_router(router)

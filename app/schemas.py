from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# --- Base Schemas (for input data) ---

class FacultyBase(BaseModel):
    name: str = Field(..., example="Computer Science")

class DepartmentBase(BaseModel):
    name: str = Field(..., example="Software Engineering")

class TeacherBase(BaseModel):
    name: str = Field(..., example="Dr. Alan Turing")

class GroupBase(BaseModel):
    code: str = Field(..., example="CS-101")
    course: int = Field(..., gt=0, example=1)
    num_students: int = Field(..., gt=0, example=25)
    faculty_id: int

class SubjectBase(BaseModel):
    name: str = Field(..., example="Introduction to Algorithms")
    num_hours: int = Field(..., gt=0, example=64)
    department_id: int
    extra: Optional[dict] = Field(None, example={"notes": "Covers basic data structures and complexity."})

class SessionBase(BaseModel):
    group_id: int
    subject_id: int
    teacher_id: int
    control_type: str = Field(..., example="exam")
    session_date: date


# --- Create Schemas (for POST requests) ---

class FacultyCreate(FacultyBase):
    pass

class DepartmentCreate(DepartmentBase):
    pass

class TeacherCreate(TeacherBase):
    pass

class GroupCreate(GroupBase):
    pass

class SubjectCreate(SubjectBase):
    pass

class SessionCreate(SessionBase):
    pass


# --- "Read" Schemas (for GET responses, with IDs) ---

class Faculty(FacultyBase):
    id: int
    class Config:
        orm_mode = True

class Department(DepartmentBase):
    id: int
    class Config:
        orm_mode = True

class Teacher(TeacherBase):
    id: int
    class Config:
        orm_mode = True

class Group(GroupBase):
    id: int
    class Config:
        orm_mode = True

class Subject(SubjectBase):
    id: int
    class Config:
        orm_mode = True

class Session(SessionBase):
    id: int
    class Config:
        orm_mode = True

# --- Schemas for Complex Responses (with nested objects) ---

class GroupDetails(Group):
    faculty: Faculty

class SubjectDetails(Subject):
    department: Department

class SessionDetails(Session):
    group: Group
    subject: Subject
    teacher: Teacher

class FacultyStats(BaseModel):
    faculty_name: str
    total_students: int
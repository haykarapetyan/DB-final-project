from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Date
from sqlalchemy.orm import relationship

from .database import Base

class Faculty(Base):
    __tablename__ = 'faculties'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    
    groups = relationship("Group", back_populates="faculty")

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    course = Column(Integer, nullable=False)
    num_students = Column(Integer, nullable=False)
    
    faculty_id = Column(Integer, ForeignKey('faculties.id'))
    faculty = relationship("Faculty", back_populates="groups")
    
    sessions = relationship("Session", back_populates="group")

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    
    subjects = relationship("Subject", back_populates="department")

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    num_hours = Column(Integer, nullable=False)
    extra = Column(JSON)
    
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship("Department", back_populates="subjects")
    
    sessions = relationship("Session", back_populates="subject")

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    
    sessions = relationship("Session", back_populates="teacher")

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True, index=True)
    control_type = Column(String, nullable=False)
    session_date = Column(Date, nullable=False)
    
    group_id = Column(Integer, ForeignKey('groups.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    
    group = relationship("Group", back_populates="sessions")
    subject = relationship("Subject", back_populates="sessions")
    teacher = relationship("Teacher", back_populates="sessions")
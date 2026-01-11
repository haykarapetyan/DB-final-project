"""create initial tables

Revision ID: 0001_create_tables
Revises: 
Create Date: 2025-12-30
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_create_tables'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # faculties
    op.create_table(
        'faculties',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
    )
    op.create_index(op.f('ix_faculties_name'), 'faculties', ['name'], unique=True)

    # departments
    op.create_table(
        'departments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
    )
    op.create_index(op.f('ix_departments_name'), 'departments', ['name'], unique=True)

    # teachers
    op.create_table(
        'teachers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
    )
    op.create_index(op.f('ix_teachers_name'), 'teachers', ['name'], unique=False)

    # groups
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('course', sa.Integer, nullable=False),
        sa.Column('num_students', sa.Integer, nullable=False),
        sa.Column('faculty_id', sa.Integer, sa.ForeignKey('faculties.id'), nullable=False),
    )
    op.create_index(op.f('ix_groups_code'), 'groups', ['code'], unique=True)

    # subjects
    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('num_hours', sa.Integer, nullable=False),
        sa.Column('extra', sa.JSON(), nullable=True),
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=False),
    )
    op.create_index(op.f('ix_subjects_name'), 'subjects', ['name'], unique=True)

    # sessions
    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('control_type', sa.String(100), nullable=False),
        sa.Column('session_date', sa.Date, nullable=False),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id'), nullable=False),
        sa.Column('subject_id', sa.Integer, sa.ForeignKey('subjects.id'), nullable=False),
        sa.Column('teacher_id', sa.Integer, sa.ForeignKey('teachers.id'), nullable=False),
    )

def downgrade():
    op.drop_table('sessions')
    op.drop_table('subjects')
    op.drop_index(op.f('ix_groups_code'), table_name='groups')
    op.drop_table('groups')

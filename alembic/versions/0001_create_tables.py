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
    op.create_table(
        'groups',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('code', sa.String(50), nullable=False),
        sa.Column('course', sa.Integer),
        sa.Column('faculty', sa.String(200)),
        sa.Column('number_of_students', sa.Integer),
    )
    op.create_index(op.f('ix_groups_code'), 'groups', ['code'], unique=False)

    op.create_table(
        'subjects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('department', sa.String(200)),
        sa.Column('hours', sa.Integer),
    )

    op.create_table(
        'sessions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('group_id', sa.Integer, sa.ForeignKey('groups.id'), nullable=False),
        sa.Column('subject_id', sa.Integer, sa.ForeignKey('subjects.id'), nullable=False),
        sa.Column('teacher', sa.String(200)),
        sa.Column('control_type', sa.String(100)),
        sa.Column('date', sa.Date),
    )

def downgrade():
    op.drop_table('sessions')
    op.drop_table('subjects')
    op.drop_index(op.f('ix_groups_code'), table_name='groups')
    op.drop_table('groups')

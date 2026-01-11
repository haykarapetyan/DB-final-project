"""add extra json column and create pg_trgm GIN index on notes

Revision ID: 0002_add_extra_and_trgm_index
Revises: 0001_create_tables
Create Date: 2025-12-30
"""
from alembic import op
import sqlalchemy as sa

revision = '0002_add_extra_and_trgm_index'
down_revision = '0001_create_tables'
branch_labels = None
depends_on = None

def upgrade():
    # Ensure pg_trgm extension exists and create trigram GIN index on subject notes
    op.execute('CREATE EXTENSION IF NOT EXISTS pg_trgm')
    op.execute("CREATE INDEX IF NOT EXISTS idx_subject_notes_trgm ON subjects USING gin ((extra->>'notes') gin_trgm_ops);")

def downgrade():
    op.execute('DROP INDEX IF EXISTS idx_subject_notes_trgm')

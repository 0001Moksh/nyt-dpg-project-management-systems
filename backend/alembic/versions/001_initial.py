"""Initial migration - Create all tables

Revision ID: 001_initial
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # All tables are created by SQLAlchemy in app.db.database.py
    # when app starts (Base.metadata.create_all(bind=engine))
    pass


def downgrade() -> None:
    pass

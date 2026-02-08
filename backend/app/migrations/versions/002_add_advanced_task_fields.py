"""Add advanced task fields

Revision ID: 002
Revises: ba8c1400deb3
Create Date: 2026-02-04 00:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel  # Added for SQLModel types


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, Sequence[str], None] = 'ba8c1400deb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to add advanced task fields."""
    # Check if columns exist before adding them to avoid duplicate column errors
    # Get existing columns in the task table
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    columns = [col['name'] for col in inspector.get_columns('task')]

    # Add columns to the existing task table only if they don't exist
    if 'priority' not in columns:
        op.add_column('task', sa.Column('priority', sa.String(length=20), server_default='medium', nullable=False))
    if 'due_date' not in columns:
        op.add_column('task', sa.Column('due_date', sa.DateTime(), nullable=True))
    if 'reminder_time' not in columns:
        op.add_column('task', sa.Column('reminder_time', sa.DateTime(), nullable=True))
    if 'category' not in columns:
        op.add_column('task', sa.Column('category', sa.String(length=50), nullable=True))
    if 'is_recurring' not in columns:
        op.add_column('task', sa.Column('is_recurring', sa.Boolean(), server_default='false', nullable=False))
    if 'recurrence_pattern' not in columns:
        op.add_column('task', sa.Column('recurrence_pattern', sa.String(length=20), nullable=True))
    if 'next_occurrence' not in columns:
        op.add_column('task', sa.Column('next_occurrence', sa.DateTime(), nullable=True))
    if 'end_recurrence' not in columns:
        op.add_column('task', sa.Column('end_recurrence', sa.DateTime(), nullable=True))
    if 'parent_task_id' not in columns:
        op.add_column('task', sa.Column('parent_task_id', sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema to remove advanced task fields."""
    # Remove columns from the task table
    # We'll attempt to drop columns regardless of whether they exist to maintain consistency
    try:
        op.drop_column('task', 'parent_task_id')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'end_recurrence')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'next_occurrence')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'recurrence_pattern')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'is_recurring')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'category')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'reminder_time')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'due_date')
    except:
        pass  # Ignore if column doesn't exist
    try:
        op.drop_column('task', 'priority')
    except:
        pass  # Ignore if column doesn't exist
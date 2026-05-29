"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-05-28

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "0001_initial_schema"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    project_priority = postgresql.ENUM("LOW", "MEDIUM", "HIGH", "CRITICAL", name="project_priority")
    project_status = postgresql.ENUM("PLANNED", "IN_PROGRESS", "COMPLETED", "ON_HOLD", "CANCELLED", name="project_status")
    project_priority.create(op.get_bind(), checkfirst=True)
    project_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "workers",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("department", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=255), nullable=False),
        sa.Column("years_experience", sa.Integer(), nullable=False),
        sa.Column("availability", sa.Boolean(), nullable=False),
        sa.Column("current_workload", sa.Integer(), nullable=False),
        sa.Column("resume", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "projects",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("timeline_start", sa.Date(), nullable=True),
        sa.Column("timeline_end", sa.Date(), nullable=True),
        sa.Column("budget", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.Column("priority", postgresql.ENUM("LOW", "MEDIUM", "HIGH", "CRITICAL", name="project_priority", create_type=False), nullable=False),
        sa.Column("status", postgresql.ENUM("PLANNED", "IN_PROGRESS", "COMPLETED", "ON_HOLD", "CANCELLED", name="project_status", create_type=False), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "project_workers",
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("worker_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role_in_project", sa.String(length=255), nullable=True),
        sa.Column("assigned_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["worker_id"], ["workers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("project_id", "worker_id"),
    )


def downgrade() -> None:
    op.drop_table("project_workers")
    op.drop_table("projects")
    op.drop_table("workers")

    project_status = postgresql.ENUM(name="project_status")
    project_priority = postgresql.ENUM(name="project_priority")
    project_status.drop(op.get_bind(), checkfirst=True)
    project_priority.drop(op.get_bind(), checkfirst=True)

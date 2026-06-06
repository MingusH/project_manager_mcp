import uuid
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.connection import Base


class ProjectPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ProjectStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(100), nullable=False)
    years_experience: Mapped[int] = mapped_column(Integer, default=0)
    availability: Mapped[bool] = mapped_column(default=True)
    current_workload: Mapped[int] = mapped_column(Integer, default=0)
    resume: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationship to projects
    projects: Mapped[list["Project"]] = relationship(
        "Project", secondary="project_workers", back_populates="workers"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    timeline_start: Mapped[date | None] = mapped_column(Date, nullable=True)
    timeline_end: Mapped[date | None] = mapped_column(Date, nullable=True)
    budget: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)
    priority: Mapped[ProjectPriority] = mapped_column(
        SqlEnum(ProjectPriority, name="projectpriority"), default=ProjectPriority.MEDIUM
    )
    status: Mapped[ProjectStatus] = mapped_column(
        SqlEnum(ProjectStatus, name="projectstatus"), default=ProjectStatus.PLANNED
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    # Relationship to workers
    workers: Mapped[list["Worker"]] = relationship(
        "Worker", secondary="project_workers", back_populates="projects"
    )


class ProjectWorker(Base):
    __tablename__ = "project_workers"

    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id"), primary_key=True
    )
    worker_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("workers.id"), primary_key=True
    )
    role_in_project: Mapped[str | None] = mapped_column(String(100), nullable=True)
    assigned_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

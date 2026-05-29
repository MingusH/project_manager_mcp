import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Project, ProjectPriority, ProjectStatus, ProjectWorker, Worker


def _project_to_dict(project: Project) -> dict:
    return {
        "id": str(project.id),
        "name": project.name,
        "description": project.description,
        "timeline_start": project.timeline_start.isoformat() if project.timeline_start else None,
        "timeline_end": project.timeline_end.isoformat() if project.timeline_end else None,
        "budget": float(project.budget) if project.budget else None,
        "priority": project.priority.value,
        "status": project.status.value,
        "created_at": project.created_at.isoformat() if project.created_at else None,
        "updated_at": project.updated_at.isoformat() if project.updated_at else None,
        "workers": [
            {
                "worker_id": str(assignment.worker_id),
                "worker_name": assignment.worker.name,
                "role_in_project": assignment.role_in_project,
                "assigned_at": assignment.assigned_at.isoformat() if assignment.assigned_at else None,
            }
            for assignment in project.worker_assignments
        ],
    }


def create_project(
    name: str,
    description: str,
    timeline_start: str | None = None,
    timeline_end: str | None = None,
    budget: float | None = None,
    priority: str = "medium",
    status: str = "planned",
) -> dict:
    with next(get_session()) as session:
        project = Project(
            name=name,
            description=description,
            timeline_start=date.fromisoformat(timeline_start) if timeline_start else None,
            timeline_end=date.fromisoformat(timeline_end) if timeline_end else None,
            budget=Decimal(str(budget)) if budget else None,
            priority=ProjectPriority(priority.lower()),
            status=ProjectStatus(status.lower().replace(" ", "_")),
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        return _project_to_dict(project)


def get_project(project_id: str) -> dict | None:
    with next(get_session()) as session:
        project = session.get(Project, uuid.UUID(project_id))
        if project is None:
            return None
        return _project_to_dict(project)


def list_projects(
    status: str | None = None,
    priority: str | None = None,
    name_contains: str | None = None,
) -> list[dict]:
    with next(get_session()) as session:
        query = select(Project)

        if status:
            query = query.where(Project.status == ProjectStatus(status.lower().replace(" ", "_")))
        if priority:
            query = query.where(Project.priority == ProjectPriority(priority.lower()))
        if name_contains:
            query = query.where(Project.name.ilike(f"%{name_contains}%"))

        projects = session.execute(query).scalars().all()
        return [_project_to_dict(p) for p in projects]


def update_project(
    project_id: str,
    name: str | None = None,
    description: str | None = None,
    timeline_start: str | None = None,
    timeline_end: str | None = None,
    budget: float | None = None,
    priority: str | None = None,
    status: str | None = None,
) -> dict | None:
    with next(get_session()) as session:
        project = session.get(Project, uuid.UUID(project_id))
        if project is None:
            return None

        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        if timeline_start is not None:
            project.timeline_start = date.fromisoformat(timeline_start)
        if timeline_end is not None:
            project.timeline_end = date.fromisoformat(timeline_end)
        if budget is not None:
            project.budget = Decimal(str(budget))
        if priority is not None:
            project.priority = ProjectPriority(priority.lower())
        if status is not None:
            project.status = ProjectStatus(status.lower().replace(" ", "_"))

        session.commit()
        session.refresh(project)
        return _project_to_dict(project)


def delete_project(project_id: str) -> bool:
    with next(get_session()) as session:
        project = session.get(Project, uuid.UUID(project_id))
        if project is None:
            return False
        session.delete(project)
        session.commit()
        return True


def add_worker_to_project(project_id: str, worker_id: str, role_in_project: str | None = None) -> dict | None:
    with next(get_session()) as session:
        project = session.get(Project, uuid.UUID(project_id))
        if project is None:
            return None

        worker = session.get(Worker, uuid.UUID(worker_id))
        if worker is None:
            return None

        assignment = ProjectWorker(
            project_id=uuid.UUID(project_id),
            worker_id=uuid.UUID(worker_id),
            role_in_project=role_in_project,
        )
        session.add(assignment)
        session.commit()
        session.refresh(project)
        return _project_to_dict(project)


def remove_worker_from_project(project_id: str, worker_id: str) -> bool:
    with next(get_session()) as session:
        assignment = session.get(ProjectWorker, (uuid.UUID(project_id), uuid.UUID(worker_id)))
        if assignment is None:
            return False
        session.delete(assignment)
        session.commit()
        return True

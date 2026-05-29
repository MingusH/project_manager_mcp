import uuid
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import Worker


def _worker_to_dict(worker: Worker) -> dict:
    return {
        "id": str(worker.id),
        "name": worker.name,
        "department": worker.department,
        "role": worker.role,
        "years_experience": worker.years_experience,
        "availability": worker.availability,
        "current_workload": worker.current_workload,
        "resume": worker.resume,
        "created_at": worker.created_at.isoformat() if worker.created_at else None,
        "updated_at": worker.updated_at.isoformat() if worker.updated_at else None,
    }


def create_worker(
    name: str,
    department: str,
    role: str,
    years_experience: int = 0,
    availability: bool = True,
    current_workload: int = 0,
    resume: str | None = None,
) -> dict:
    with next(get_session()) as session:
        worker = Worker(
            name=name,
            department=department,
            role=role,
            years_experience=years_experience,
            availability=availability,
            current_workload=current_workload,
            resume=resume,
        )
        session.add(worker)
        session.commit()
        session.refresh(worker)
        return _worker_to_dict(worker)


def get_worker(worker_id: str) -> dict | None:
    with next(get_session()) as session:
        worker = session.get(Worker, uuid.UUID(worker_id))
        if worker is None:
            return None
        return _worker_to_dict(worker)


def list_workers(
    department: str | None = None,
    role: str | None = None,
    availability: bool | None = None,
    min_experience: int | None = None,
    max_workload: int | None = None,
) -> list[dict]:
    with next(get_session()) as session:
        query = select(Worker)

        if department:
            query = query.where(Worker.department == department)
        if role:
            query = query.where(Worker.role == role)
        if availability is not None:
            query = query.where(Worker.availability == availability)
        if min_experience is not None:
            query = query.where(Worker.years_experience >= min_experience)
        if max_workload is not None:
            query = query.where(Worker.current_workload <= max_workload)

        workers = session.execute(query).scalars().all()
        return [_worker_to_dict(w) for w in workers]


def update_worker(
    worker_id: str,
    name: str | None = None,
    department: str | None = None,
    role: str | None = None,
    years_experience: int | None = None,
    availability: bool | None = None,
    current_workload: int | None = None,
    resume: str | None = None,
) -> dict | None:
    with next(get_session()) as session:
        worker = session.get(Worker, uuid.UUID(worker_id))
        if worker is None:
            return None

        if name is not None:
            worker.name = name
        if department is not None:
            worker.department = department
        if role is not None:
            worker.role = role
        if years_experience is not None:
            worker.years_experience = years_experience
        if availability is not None:
            worker.availability = availability
        if current_workload is not None:
            worker.current_workload = current_workload
        if resume is not None:
            worker.resume = resume

        session.commit()
        session.refresh(worker)
        return _worker_to_dict(worker)


def delete_worker(worker_id: str) -> bool:
    with next(get_session()) as session:
        worker = session.get(Worker, uuid.UUID(worker_id))
        if worker is None:
            return False
        session.delete(worker)
        session.commit()
        return True

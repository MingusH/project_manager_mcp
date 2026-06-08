"""Dashboard API - FastAPI application with WebSocket support."""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, List, Set

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from src.database import get_session, create_database_tables, Project, ProjectStatus, ProjectWorker, Worker

# Store active WebSocket connections
active_connections: Set[WebSocket] = set()


async def broadcast_update(update_type: str, data: dict):
    """Broadcast update to all connected WebSocket clients."""
    global active_connections
    message = {
        "type": update_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": data
    }
    disconnected = set()
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.add(connection)
    # Remove disconnected clients
    active_connections -= disconnected


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Dashboard API starting...")
    try:
        create_database_tables()
        print("Database tables verified.")
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
    yield
    # Shutdown
    print("Dashboard API shutting down...")
    for conn in active_connections:
        await conn.close()


app = FastAPI(
    title="Project Manager Dashboard API",
    description="Real-time dashboard API for project and worker management",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Project Manager Dashboard API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}


@app.get("/api/metrics")
async def get_metrics():
    """Get overview metrics."""
    with next(get_session()) as session:
        total_workers = session.scalar(select(func.count()).select_from(Worker))
        total_projects = session.scalar(select(func.count()).select_from(Project))
        active_projects = session.scalar(
            select(func.count()).select_from(Project).where(Project.status == ProjectStatus.IN_PROGRESS)
        )
        completed_projects = session.scalar(
            select(func.count()).select_from(Project).where(Project.status == ProjectStatus.COMPLETED)
        )
        available_workers = session.scalar(
            select(func.count()).select_from(Worker).where(Worker.availability == True)
        )

        # Department breakdown
        dept_query = select(Worker.department, func.count()).group_by(Worker.department)
        dept_results = session.execute(dept_query).all()
        department_breakdown = {dept: count for dept, count in dept_results}

        return {
            "total_workers": total_workers,
            "total_projects": total_projects,
            "active_projects": active_projects,
            "completed_projects": completed_projects,
            "available_workers": available_workers,
            "department_breakdown": department_breakdown
        }


@app.get("/api/workers")
async def get_workers(
    department: str = None,
    role: str = None,
    availability: bool = None,
    min_experience: int = None
):
    """Get workers with optional filters."""
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

        workers = session.execute(query).scalars().all()

        return [
            {
                "id": str(w.id),
                "name": w.name,
                "department": w.department,
                "role": w.role,
                "years_experience": w.years_experience,
                "availability": w.availability,
                "current_workload": w.current_workload,
                "created_at": w.created_at.isoformat() if w.created_at else None,
            }
            for w in workers
        ]


@app.get("/api/workers/{worker_id}")
async def get_worker(worker_id: str):
    """Get a single worker by ID."""
    import uuid
    with next(get_session()) as session:
        worker = session.get(Worker, uuid.UUID(worker_id))
        if not worker:
            return {"error": "Worker not found"}, 404

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


@app.get("/api/projects")
async def get_projects(
    status: str = None,
    priority: str = None,
    name_contains: str = None
):
    """Get projects with optional filters."""
    with next(get_session()) as session:
        query = select(Project).options(selectinload(Project.workers))

        if status:
            query = query.where(Project.status == ProjectStatus(status.lower().replace(" ", "_")))
        if priority:
            from src.models import ProjectPriority
            query = query.where(Project.priority == ProjectPriority(priority.lower()))
        if name_contains:
            query = query.where(Project.name.ilike(f"%{name_contains}%"))

        projects = session.execute(query).scalars().all()

        return [
            {
                "id": str(p.id),
                "name": p.name,
                "description": p.description,
                "timeline_start": p.timeline_start.isoformat() if p.timeline_start else None,
                "timeline_end": p.timeline_end.isoformat() if p.timeline_end else None,
                "budget": float(p.budget) if p.budget else None,
                "priority": p.priority.value,
                "status": p.status.value,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "worker_count": len(p.workers),
                "workers": [
                    {"id": str(w.id), "name": w.name}
                    for w in p.workers
                ]
            }
            for p in projects
        ]


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str):
    """Get a single project by ID with full worker details."""
    import uuid
    with next(get_session()) as session:
        project = session.get(
            Project,
            uuid.UUID(project_id),
            options=[selectinload(Project.workers)]
        )
        if not project:
            return {"error": "Project not found"}, 404

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
                    "id": str(w.id),
                    "name": w.name,
                }
                for w in project.workers
            ]
        }


@app.get("/api/departments")
async def get_departments():
    """Get list of all departments and worker counts."""
    with next(get_session()) as session:
        query = select(Worker.department, func.count()).group_by(Worker.department)
        results = session.execute(query).all()
        return [
            {"name": dept, "worker_count": count}
            for dept, count in results
        ]


@app.post("/internal/notify")
async def notify_update(update_type: str = "refresh"):
    """Internal endpoint for MCP tools to notify dashboard of changes."""
    await broadcast_update(update_type, {})
    return {"status": "notified"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time updates."""
    await websocket.accept()
    active_connections.add(websocket)
    print(f"WebSocket client connected. Total: {len(active_connections)}")

    try:
        # Send initial data
        metrics = await get_metrics()
        await websocket.send_json({"type": "metrics", "data": metrics})

        # Keep connection alive and handle incoming messages
        while True:
            try:
                message = await asyncio.wait_for(
                    websocket.receive_json(),
                    timeout=30.0
                )

                # Handle subscription requests
                if message.get("action") == "subscribe":
                    channel = message.get("channel")
                    if channel == "overview":
                        metrics = await get_metrics()
                        await websocket.send_json({"type": "metrics", "data": metrics})
                    elif channel == "workers":
                        workers = await get_workers()
                        await websocket.send_json({"type": "workers", "data": workers})
                    elif channel == "projects":
                        projects = await get_projects()
                        await websocket.send_json({"type": "projects", "data": projects})

                elif message.get("action") == "ping":
                    await websocket.send_json({"type": "pong"})

            except asyncio.TimeoutError:
                # Send heartbeat to keep connection alive
                await websocket.send_json({"type": "heartbeat"})

    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        active_connections.discard(websocket)
        print(f"Client removed. Total: {len(active_connections)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

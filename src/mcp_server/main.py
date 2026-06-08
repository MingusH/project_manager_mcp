from mcp.server.fastmcp import FastMCP

from src.config import settings
from src.database import check_database_connection
from src.mcp_server.tools import workers
from src.mcp_server.tools import projects


mcp = FastMCP(settings.mcp_server_name)


@mcp.tool()
def health_check() -> dict[str, str]:
    database = check_database_connection()

    return {
        "status": "ok",
        "server": settings.mcp_server_name,
        "version": settings.mcp_server_version,
        "database": database["status"],
    }


@mcp.tool()
def server_info() -> dict[str, str]:
    return {
        "name": settings.mcp_server_name,
        "version": settings.mcp_server_version,
        "database_host": settings.postgres_host,
        "database_name": settings.postgres_db,
    }


@mcp.tool()
def create_worker(
    name: str,
    department: str,
    role: str,
    years_experience: int = 0,
    availability: bool = True,
    current_workload: int = 0,
    resume: str | None = None,
) -> dict:
    return workers.create_worker(name, department, role, years_experience, availability, current_workload, resume)


@mcp.tool()
def get_worker(worker_id: str) -> dict | None:
    return workers.get_worker(worker_id)


@mcp.tool()
def list_workers(
    department: str | None = None,
    role: str | None = None,
    availability: bool | None = None,
    min_experience: int | None = None,
    max_workload: int | None = None,
) -> list[dict]:
    return workers.list_workers(department, role, availability, min_experience, max_workload)


@mcp.tool()
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
    return workers.update_worker(worker_id, name, department, role, years_experience, availability, current_workload, resume)


@mcp.tool()
def delete_worker(worker_id: str) -> bool:
    return workers.delete_worker(worker_id)


@mcp.tool()
def create_project(
    name: str,
    description: str,
    timeline_start: str | None = None,
    timeline_end: str | None = None,
    budget: float | None = None,
    priority: str = "medium",
    status: str = "planned",
) -> dict:
    return projects.create_project(name, description, timeline_start, timeline_end, budget, priority, status)


@mcp.tool()
def get_project(project_id: str) -> dict | None:
    return projects.get_project(project_id)


@mcp.tool()
def list_projects(
    status: str | None = None,
    priority: str | None = None,
    name_contains: str | None = None,
) -> list[dict]:
    return projects.list_projects(status, priority, name_contains)


@mcp.tool()
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
    return projects.update_project(project_id, name, description, timeline_start, timeline_end, budget, priority, status)


@mcp.tool()
def delete_project(project_id: str) -> bool:
    return projects.delete_project(project_id)


@mcp.tool()
def add_worker_to_project(project_id: str, worker_id: str, role_in_project: str | None = None) -> dict | None:
    return projects.add_worker_to_project(project_id, worker_id, role_in_project)


@mcp.tool()
def remove_worker_from_project(project_id: str, worker_id: str) -> bool:
    return projects.remove_worker_from_project(project_id, worker_id)


if __name__ == "__main__":
    import os
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    if transport == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run()

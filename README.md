# Project Manager MCP Server

A Python-based MCP (Model Context Protocol) server for managing company projects and workers with PostgreSQL storage. Designed for integration with Claude Desktop for AI-powered project management.

## Features

- **Worker Management**: Create, read, update, delete workers with attributes like department, role, experience, availability, and workload
- **Project Management**: Full project lifecycle management with timeline, budget, priority, and status tracking
- **Worker Assignment**: Assign workers to projects with specific roles
- **AI Integration**: Works seamlessly with Claude Desktop for intelligent worker assignment based on project requirements
- **Dockerized**: Complete containerized setup with PostgreSQL and MCP server

## Architecture

- **Language**: Python 3.11+
- **MCP Framework**: Python MCP SDK (stdio transport)
- **Database**: PostgreSQL 15 with SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **Deployment**: Docker Compose (MCP server + PostgreSQL)

## Quick Start

### Prerequisites

- Docker Desktop installed and running
- Docker Compose
- Claude Desktop (for AI integration)

### 1. Clone and Setup

```powershell
git clone https://github.com/MingusH/project_manager_mcp.git
cd project_manager_mcp
```

### 2. Environment Configuration

Copy the example environment file:

```powershell
cp .env.example .env
```

Edit `.env` with your settings (defaults work out of the box):

```env
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=project_manager
POSTGRES_USER=project_user
POSTGRES_PASSWORD=project_password
MCP_SERVER_NAME=project-manager
MCP_SERVER_VERSION=0.1.0
```

### 3. Start Services

```powershell
docker compose up --build -d
```

### 4. Run Database Migrations

```powershell
docker compose run --rm mcp-server alembic upgrade head
```

### 5. Verify Setup

Check database tables:

```powershell
docker compose exec postgres psql -U project_user -d project_manager -c "\dt"
```

Verify MCP server health:

```powershell
docker run --rm --network projectmanager_project-manager-network -v ".\src:/app/src" -e POSTGRES_HOST=postgres -e POSTGRES_PORT=5432 -e POSTGRES_DB=project_manager -e POSTGRES_USER=project_user -e POSTGRES_PASSWORD=project_password projectmanager-mcp-server python -c "from src.main import mcp; print('OK')"
```

## Claude Desktop Integration

### Configure MCP Server

Add to your Claude Desktop config (`claude_desktop_config.json`):

**Windows (PowerShell config location):**
```powershell
C:\Users\<username>\AppData\Roaming\Claude\claude_desktop_config.json
```

**Config content:**
```json
{
  "mcpServers": {
    "project-manager": {
      "command": "C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe",
      "args": [
        "run",
        "--rm",
        "-i",
        "--network",
        "projectmanager_project-manager-network",
        "-v",
        "C:\\Users\\<username>\\OneDrive - EFIF\\Skrivebord\\projectManager\\src:/app/src",
        "-e",
        "POSTGRES_HOST=postgres",
        "-e",
        "POSTGRES_PORT=5432",
        "-e",
        "POSTGRES_DB=project_manager",
        "-e",
        "POSTGRES_USER=project_user",
        "-e",
        "POSTGRES_PASSWORD=project_password",
        "projectmanager-mcp-server",
        "python",
        "-m",
        "src.main"
      ]
    }
  }
}
```

**Note:** Update the volume path to match your project location.

### Restart Claude Desktop

After updating the config, fully quit and reopen Claude Desktop. The MCP server will appear in the tools menu.

## MCP Tools Reference

### System Tools
| Tool | Description |
|------|-------------|
| `health_check` | Verify server and database connection status |
| `server_info` | Get server name, version, and database config |

### Worker Management
| Tool | Description |
|------|-------------|
| `create_worker` | Create a new worker with name, department, role, experience, availability |
| `get_worker` | Retrieve worker details by ID |
| `list_workers` | List all workers with optional filters (department, role, availability, experience, workload) |
| `update_worker` | Update worker attributes |
| `delete_worker` | Delete a worker by ID |

### Project Management
| Tool | Description |
|------|-------------|
| `create_project` | Create a new project with name, description, timeline, budget, priority, status |
| `get_project` | Retrieve project details including assigned workers |
| `list_projects` | List all projects with optional filters (status, priority, name search) |
| `update_project` | Update project attributes |
| `delete_project` | Delete a project by ID |
| `add_worker_to_project` | Assign a worker to a project with optional role |
| `remove_worker_from_project` | Remove a worker from a project |

## Usage Examples

### Create a Worker
```text
Use the project-manager MCP server to create a worker named "Alice Johnson" in the Engineering department with role "Senior Developer", 5 years of experience, and availability true.
```

### Create a Project
```text
Create a project called "Website Redesign" with description "Complete overhaul of company website", priority "high", budget 50000, and timeline from 2024-01-01 to 2024-06-01.
```

### Assign Worker to Project
```text
Add worker Alice to the Website Redesign project as "Lead Frontend Developer".
```

### List Available Workers
```text
List all workers in the Engineering department with availability true and at least 3 years of experience.
```

## Database Schema

### Workers Table
- `id` (UUID, PK)
- `name` (string)
- `department` (string)
- `role` (string)
- `years_experience` (integer)
- `availability` (boolean)
- `current_workload` (integer, 0-100)
- `resume` (text)
- `created_at`, `updated_at` (timestamps)

### Projects Table
- `id` (UUID, PK)
- `name` (string)
- `description` (text)
- `timeline_start`, `timeline_end` (dates)
- `budget` (decimal)
- `priority` (enum: low, medium, high, critical)
- `status` (enum: planned, in_progress, completed, on_hold, cancelled)
- `created_at`, `updated_at` (timestamps)

### Project_Workers Junction Table
- `project_id` (UUID, FK)
- `worker_id` (UUID, FK)
- `role_in_project` (string)
- `assigned_at` (timestamp)

## Development

### Project Structure
```
projectManager/
├── Dockerfile               # MCP server container
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore             # Git ignore rules
├── README.md              # This file
├── alembic/                # Database migrations
│   ├── versions/
│   └── env.py
├── src/
│   ├── __init__.py
│   ├── main.py             # MCP server entry point
│   ├── config.py           # Configuration
│   ├── database.py         # SQLAlchemy setup
│   ├── models.py           # Database models
│   └── tools/
│       ├── __init__.py
│       ├── workers.py      # Worker tools
│       └── projects.py     # Project tools
└── tests/
    └── __init__.py
```

### Common Commands

```powershell
# Start services
docker compose up -d

# View logs
docker compose logs -f mcp-server

# Stop services
docker compose down

# Rebuild after code changes
docker compose up --build --force-recreate

# Database shell
docker compose exec postgres psql -U project_user -d project_manager

# Run migrations
docker compose run --rm mcp-server alembic upgrade head

# Create new migration
docker compose run --rm mcp-server alembic revision --autogenerate -m "description"
```

## Troubleshooting

### Claude Desktop doesn't recognize the server
- Verify config file path matches your Claude Desktop installation
- Ensure Docker Desktop is running
- Check that the Docker network exists: `docker network ls`
- Try fully quitting and reopening Claude Desktop

### Database connection errors
- Verify PostgreSQL container is healthy: `docker compose ps`
- Check environment variables in docker-compose.yml
- Ensure database exists: `docker compose exec postgres psql -U project_user -l`

### MCP server crashes
- Check logs: `docker compose logs mcp-server`
- Verify all Python files compile: `python -m py_compile src\main.py`
- Ensure volume mount path is correct in Claude Desktop config

## License

MIT

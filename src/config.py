import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    postgres_host: str = os.getenv("POSTGRES_HOST", "postgres")
    postgres_port: int = int(os.getenv("POSTGRES_PORT", "5432"))
    postgres_db: str = os.getenv("POSTGRES_DB", "project_manager")
    postgres_user: str = os.getenv("POSTGRES_USER", "project_user")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD", "project_password")
    mcp_server_name: str = os.getenv("MCP_SERVER_NAME", "project-manager")
    mcp_server_version: str = os.getenv("MCP_SERVER_VERSION", "0.1.0")

    @property
    def database_url(self) -> str:
        # Use DATABASE_URL if provided (for Supabase/production), otherwise build from components
        env_url = os.getenv("DATABASE_URL")
        if env_url:
            # Convert postgresql:// to postgresql+psycopg2:// if needed
            if env_url.startswith("postgresql://"):
                return env_url.replace("postgresql://", "postgresql+psycopg2://", 1)
            return env_url
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()

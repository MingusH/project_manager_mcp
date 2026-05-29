from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_database_tables() -> None:
    from src import models

    Base.metadata.create_all(bind=engine)


def check_database_connection() -> dict[str, str]:
    with SessionLocal() as session:
        session.execute(text("SELECT 1"))

    return {"status": "ok"}

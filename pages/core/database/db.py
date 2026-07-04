import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from pages.core.database.models import Base


DEFAULT_DB_PATH = str(Path(__file__).resolve().parents[2] / "recruit_ai.db")
DB_PATH = os.getenv("RECRUITAI_DB_PATH", DEFAULT_DB_PATH)

engine = create_engine(f"sqlite:///{DB_PATH}", future=True, poolclass=NullPool, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def close_db():
    global engine, SessionLocal
    if "engine" in globals() and engine is not None:
        engine.dispose()
    if "SessionLocal" in globals() and SessionLocal is not None:
        SessionLocal.close_all()


def init_db(db_path: str | None = None):
    global DB_PATH, engine, SessionLocal

    close_db()

    if db_path is not None:
        DB_PATH = db_path
    else:
        DB_PATH = os.getenv("RECRUITAI_DB_PATH", DEFAULT_DB_PATH)

    engine = create_engine(f"sqlite:///{DB_PATH}", future=True, poolclass=NullPool, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    return engine


init_db()

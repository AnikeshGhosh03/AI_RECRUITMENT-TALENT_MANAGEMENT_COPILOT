import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import close_all_sessions, sessionmaker
from sqlalchemy.pool import NullPool

from pages.core.database.models import Base


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DB_PATH = str(PROJECT_ROOT / "recruit_ai.db")
load_dotenv(PROJECT_ROOT / ".env", override=False)
DB_PATH = os.getenv("RECRUITAI_DB_PATH", DEFAULT_DB_PATH)


def build_database_url() -> str:
    explicit_url = os.getenv("RECRUITAI_DB_URL")
    if explicit_url:
        return explicit_url

    db_type = os.getenv("RECRUITAI_DB_TYPE", "").strip().lower()
    mysql_settings_present = any(
        os.getenv(key)
        for key in ["RECRUITAI_DB_HOST", "RECRUITAI_DB_PORT", "RECRUITAI_DB_USER", "RECRUITAI_DB_PASSWORD", "RECRUITAI_DB_NAME"]
    )
    if db_type == "mysql" or mysql_settings_present:
        host = os.getenv("RECRUITAI_DB_HOST", "localhost").strip()
        port = os.getenv("RECRUITAI_DB_PORT", "3306").strip()
        user = os.getenv("RECRUITAI_DB_USER", "root").strip()
        password = os.getenv("RECRUITAI_DB_PASSWORD", "").strip()
        db_name = os.getenv("RECRUITAI_DB_NAME", "recruit_ai").strip()
        encoded_user = quote_plus(user)
        encoded_password = quote_plus(password)
        return f"mysql+pymysql://{encoded_user}:{encoded_password}@{host}:{port}/{db_name}"

    return f"sqlite:///{os.getenv('RECRUITAI_DB_PATH', DEFAULT_DB_PATH)}"


engine = None
SessionLocal = None


def close_db():
    global engine, SessionLocal
    if engine is not None:
        engine.dispose()
    if SessionLocal is not None:
        close_all_sessions()


def init_db(db_path: str | None = None, db_url: str | None = None):
    global DB_PATH, engine, SessionLocal

    close_db()

    if db_url is not None:
        database_url = db_url
    else:
        database_url = build_database_url()

    if db_path is not None:
        DB_PATH = db_path
        database_url = f"sqlite:///{DB_PATH}"

    engine_kwargs = {
        "future": True,
        "poolclass": NullPool,
        "pool_pre_ping": True,
    }
    if database_url.startswith("sqlite"):
        engine_kwargs["connect_args"] = {"check_same_thread": False}

    if database_url.startswith("mysql"):
        url = make_url(database_url)
        db_name = url.database or "recruit_ai"
        server_url = f"mysql+pymysql://{url.username or 'root'}:{quote_plus(url.password or '')}@{url.host or 'localhost'}:{url.port or 3306}"
        server_engine = create_engine(server_url, **engine_kwargs)
        with server_engine.connect() as connection:
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{db_name}`"))
        server_engine.dispose()

    engine = create_engine(database_url, **engine_kwargs)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)
    return engine


init_db()

import os

from pages.core.database import db


def test_build_database_url_prefers_explicit_url(monkeypatch):
    monkeypatch.setenv("RECRUITAI_DB_URL", "mysql+pymysql://root:pass@db:3306/recruit")
    assert db.build_database_url() == "mysql+pymysql://root:pass@db:3306/recruit"


def test_build_database_url_uses_mysql_settings(monkeypatch):
    monkeypatch.delenv("RECRUITAI_DB_URL", raising=False)
    monkeypatch.setenv("RECRUITAI_DB_TYPE", "mysql")
    monkeypatch.setenv("RECRUITAI_DB_HOST", "db")
    monkeypatch.setenv("RECRUITAI_DB_PORT", "3306")
    monkeypatch.setenv("RECRUITAI_DB_USER", "root")
    monkeypatch.setenv("RECRUITAI_DB_PASSWORD", "secret")
    monkeypatch.setenv("RECRUITAI_DB_NAME", "recruit")

    assert db.build_database_url() == "mysql+pymysql://root:secret@db:3306/recruit"


def test_build_database_url_url_encodes_special_characters(monkeypatch):
    monkeypatch.setenv("RECRUITAI_DB_TYPE", "mysql")
    monkeypatch.setenv("RECRUITAI_DB_HOST", "db")
    monkeypatch.setenv("RECRUITAI_DB_PORT", "3306")
    monkeypatch.setenv("RECRUITAI_DB_USER", "root")
    monkeypatch.setenv("RECRUITAI_DB_PASSWORD", "Anikesh@2004")
    monkeypatch.setenv("RECRUITAI_DB_NAME", "recruit")

    assert db.build_database_url() == "mysql+pymysql://root:Anikesh%402004@db:3306/recruit"


def test_build_database_url_defaults_to_sqlite(monkeypatch):
    monkeypatch.delenv("RECRUITAI_DB_URL", raising=False)
    monkeypatch.delenv("RECRUITAI_DB_TYPE", raising=False)
    monkeypatch.delenv("RECRUITAI_DB_HOST", raising=False)
    monkeypatch.delenv("RECRUITAI_DB_PORT", raising=False)
    monkeypatch.delenv("RECRUITAI_DB_USER", raising=False)
    monkeypatch.delenv("RECRUITAI_DB_PASSWORD", raising=False)
    monkeypatch.delenv("RECRUITAI_DB_NAME", raising=False)
    monkeypatch.delenv("RECRUITAI_DB_PATH", raising=False)

    url = db.build_database_url()

    assert url.startswith("sqlite:///")

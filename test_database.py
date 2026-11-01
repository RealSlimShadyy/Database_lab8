from sqlalchemy import inspect
from sqlalchemy.pool import StaticPool

from database import DEFAULT_URL, get_url, make_engine, make_session_factory


def test_default_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    assert get_url() == DEFAULT_URL


def test_url_from_env(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite://")
    assert get_url() == "sqlite://"


def test_tables_are_created():
    engine = make_engine("sqlite://", poolclass=StaticPool)
    make_session_factory(engine)
    assert "tasks" in inspect(engine).get_table_names()
    engine.dispose()
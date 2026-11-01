import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base

DEFAULT_URL = "postgresql+psycopg://todo:todo@localhost:5432/todo"


def get_url():
    return os.environ.get("DATABASE_URL", DEFAULT_URL)


def make_engine(url=None, **kwargs):
    return create_engine(url or get_url(), **kwargs)


def make_session_factory(engine):
    Base.metadata.create_all(engine)
    return sessionmaker(engine, expire_on_commit=False)
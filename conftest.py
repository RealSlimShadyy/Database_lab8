import pytest
from sqlalchemy.pool import StaticPool

from database import make_engine, make_session_factory
from model import TaskModel
from repository import SqlAlchemyTaskRepository


@pytest.fixture
def repo():
    engine = make_engine("sqlite://", poolclass=StaticPool)
    yield SqlAlchemyTaskRepository(make_session_factory(engine))
    engine.dispose()


@pytest.fixture
def model(repo):
    return TaskModel(repo)
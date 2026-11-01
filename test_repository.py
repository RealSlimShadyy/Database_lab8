import uuid
from datetime import datetime

import pytest

from model import Status, Task
from repository import TaskRepository

DATE = datetime(2026, 12, 1, 10, 0)


def test_repository_is_abstract():
    with pytest.raises(TypeError):
        TaskRepository()


def test_add_and_get(repo):
    task = repo.add(Task("a", DATE))
    saved = repo.get(task.id)
    assert saved.description == "a"
    assert saved.schedule_for == DATE
    assert saved.status == Status.TODO
    assert saved.created_at is not None


def test_get_unknown(repo):
    assert repo.get(uuid.uuid4()) is None


def test_list_all_empty(repo):
    assert repo.list_all() == []


def test_list_all(repo):
    repo.add(Task("a", DATE))
    repo.add(Task("b", DATE))
    assert len(repo.list_all()) == 2


def test_list_by_status(repo):
    a = repo.add(Task("a", DATE))
    b = repo.add(Task("b", DATE))
    repo.update(b.id, status=Status.IN_PROGRESS)
    assert [t.id for t in repo.list_by_status(Status.TODO)] == [a.id]
    assert [t.id for t in repo.list_by_status(Status.IN_PROGRESS)] == [b.id]
    assert repo.list_by_status(Status.DONE) == []


def test_update_fields(repo):
    task = repo.add(Task("a", DATE))
    new_date = datetime(2027, 1, 1, 8, 30)
    repo.update(task.id, description="b", schedule_for=new_date)
    saved = repo.get(task.id)
    assert saved.description == "b"
    assert saved.schedule_for == new_date


def test_update_status(repo):
    task = repo.add(Task("a", DATE))
    repo.update(task.id, status=Status.DONE)
    assert repo.get(task.id).status == Status.DONE


def test_update_nothing_changes(repo):
    task = repo.add(Task("a", DATE))
    repo.update(task.id)
    saved = repo.get(task.id)
    assert saved.description == "a"
    assert saved.schedule_for == DATE


def test_update_unknown(repo):
    assert repo.update(uuid.uuid4(), description="x") is None


def test_delete(repo):
    task = repo.add(Task("a", DATE))
    assert repo.delete(task.id) is True
    assert repo.get(task.id) is None


def test_delete_unknown(repo):
    assert repo.delete(uuid.uuid4()) is False
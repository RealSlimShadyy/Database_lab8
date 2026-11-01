import uuid
from datetime import datetime

import pytest

from model import Status

DATE = datetime(2026, 12, 1, 10, 0)


def test_add_task_defaults(model):
    task = model.add("Купити хліб", DATE)
    assert task.status == Status.TODO
    assert task.schedule_for == DATE
    assert task.created_at is not None
    assert len(model.all()) == 1


def test_add_strips_description(model):
    task = model.add("  Купити хліб  ", DATE)
    assert model.get(task.id).description == "Купити хліб"


def test_add_empty_description(model):
    with pytest.raises(ValueError):
        model.add("   ", DATE)


def test_ids_are_unique(model):
    a = model.add("a", DATE)
    b = model.add("b", DATE)
    assert a.id != b.id


def test_find_by_full_id(model):
    task = model.add("a", DATE)
    assert model.find(str(task.id)).id == task.id


def test_find_by_prefix(model):
    task = model.add("a", DATE)
    assert model.find(str(task.id)[:8]).id == task.id


def test_find_unknown(model):
    model.add("a", DATE)
    assert model.find("zzzz") is None


def test_find_empty_string(model):
    model.add("a", DATE)
    assert model.find("") is None


def test_set_status(model):
    task = model.add("a", DATE)
    model.set_status(task.id, Status.DONE)
    assert model.get(task.id).status == Status.DONE


def test_set_status_unknown(model):
    assert model.set_status(uuid.uuid4(), Status.DONE) is None


def test_update_description_and_date(model):
    task = model.add("a", DATE)
    new_date = datetime(2027, 1, 1, 8, 30)
    model.update(task.id, "b", new_date)
    saved = model.get(task.id)
    assert saved.description == "b"
    assert saved.schedule_for == new_date


def test_update_nothing_changes(model):
    task = model.add("a", DATE)
    model.update(task.id)
    saved = model.get(task.id)
    assert saved.description == "a"
    assert saved.schedule_for == DATE


def test_update_empty_description(model):
    task = model.add("a", DATE)
    with pytest.raises(ValueError):
        model.update(task.id, "  ")


def test_delete(model):
    task = model.add("a", DATE)
    assert model.delete(task.id) is True
    assert model.all() == []


def test_delete_unknown(model):
    assert model.delete(uuid.uuid4()) is False


def test_filter_by_status(model):
    a = model.add("a", DATE)
    b = model.add("b", DATE)
    model.set_status(b.id, Status.IN_PROGRESS)
    assert [t.id for t in model.by_status(Status.TODO)] == [a.id]
    assert [t.id for t in model.by_status(Status.IN_PROGRESS)] == [b.id]
    assert model.by_status(Status.DONE) == []
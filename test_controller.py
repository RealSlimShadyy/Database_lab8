from datetime import datetime

from controller import Controller
from model import Status
from view import ConsoleView

DATE = datetime(2026, 12, 1, 10, 0)


def feed(monkeypatch, answers):
    it = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(it))


def make_app(model):
    return Controller(model, ConsoleView())


def short_id(task):
    return str(task.id)[:8]


def test_create_task(monkeypatch, model):
    app = make_app(model)
    feed(monkeypatch, ["1", "Купити хліб", "01.12.2026 10:00", "0"])
    app.run()
    tasks = model.all()
    assert len(tasks) == 1
    assert tasks[0].description == "Купити хліб"
    assert tasks[0].schedule_for == DATE


def test_create_task_empty_description(monkeypatch, model):
    app = make_app(model)
    feed(monkeypatch, ["1", "", "0"])
    app.run()
    assert model.all() == []


def test_create_task_bad_date_then_good(monkeypatch, capsys, model):
    app = make_app(model)
    feed(monkeypatch, ["1", "Задача", "abc", "01.12.2026 10:00", "0"])
    app.run()
    assert len(model.all()) == 1
    assert "Невірний формат" in capsys.readouterr().out


def test_change_status_done(monkeypatch, model):
    app = make_app(model)
    task = model.add("a", DATE)
    feed(monkeypatch, ["2", short_id(task), "2", "0"])
    app.run()
    assert model.get(task.id).status == Status.DONE


def test_change_status_in_progress(monkeypatch, model):
    app = make_app(model)
    task = model.add("a", DATE)
    feed(monkeypatch, ["2", short_id(task), "1", "0"])
    app.run()
    assert model.get(task.id).status == Status.IN_PROGRESS


def test_change_status_wrong_choice(monkeypatch, model):
    app = make_app(model)
    task = model.add("a", DATE)
    feed(monkeypatch, ["2", short_id(task), "9", "0"])
    app.run()
    assert model.get(task.id).status == Status.TODO


def test_change_status_unknown(monkeypatch, capsys, model):
    app = make_app(model)
    feed(monkeypatch, ["2", "zzzz", "0"])
    app.run()
    assert "не знайдено" in capsys.readouterr().out


def test_delete_task(monkeypatch, model):
    app = make_app(model)
    task = model.add("a", DATE)
    feed(monkeypatch, ["3", short_id(task), "0"])
    app.run()
    assert model.all() == []


def test_delete_unknown(monkeypatch, capsys, model):
    app = make_app(model)
    model.add("a", DATE)
    feed(monkeypatch, ["3", "zzzz", "0"])
    app.run()
    assert len(model.all()) == 1
    assert "не знайдено" in capsys.readouterr().out


def test_edit_task(monkeypatch, model):
    app = make_app(model)
    task = model.add("a", DATE)
    feed(monkeypatch, ["4", short_id(task), "Нова назва", "02.12.2026 12:30", "0"])
    app.run()
    saved = model.get(task.id)
    assert saved.description == "Нова назва"
    assert saved.schedule_for == datetime(2026, 12, 2, 12, 30)


def test_edit_task_keep_values(monkeypatch, model):
    app = make_app(model)
    task = model.add("a", DATE)
    feed(monkeypatch, ["4", short_id(task), "", "", "0"])
    app.run()
    saved = model.get(task.id)
    assert saved.description == "a"
    assert saved.schedule_for == DATE


def test_edit_unknown(monkeypatch, capsys, model):
    app = make_app(model)
    feed(monkeypatch, ["4", "zzzz", "0"])
    app.run()
    assert "не знайдено" in capsys.readouterr().out


def test_list_tasks(monkeypatch, capsys, model):
    app = make_app(model)
    model.add("first_task", DATE)
    feed(monkeypatch, ["5", "0"])
    app.run()
    out = capsys.readouterr().out
    assert "first_task" in out
    assert "ToDo" in out


def test_list_empty(monkeypatch, capsys, model):
    app = make_app(model)
    feed(monkeypatch, ["5", "0"])
    app.run()
    assert "Список порожній" in capsys.readouterr().out


def test_filter_tasks(monkeypatch, capsys, model):
    app = make_app(model)
    model.add("first_task", DATE)
    second = model.add("second_task", DATE)
    model.set_status(second.id, Status.DONE)
    feed(monkeypatch, ["6", "3", "0"])
    app.run()
    out = capsys.readouterr().out
    assert "second_task" in out
    assert "first_task" not in out


def test_filter_wrong_choice(monkeypatch, capsys, model):
    app = make_app(model)
    feed(monkeypatch, ["6", "9", "0"])
    app.run()
    assert "Невірний вибір" in capsys.readouterr().out


def test_show_task(monkeypatch, capsys, model):
    app = make_app(model)
    task = model.add("first_task", DATE)
    model.add("second_task", DATE)
    feed(monkeypatch, ["7", short_id(task), "0"])
    app.run()
    out = capsys.readouterr().out
    assert "first_task" in out
    assert "second_task" not in out


def test_unknown_menu_item(monkeypatch, capsys, model):
    app = make_app(model)
    feed(monkeypatch, ["x", "0"])
    app.run()
    assert "Невірний пункт меню" in capsys.readouterr().out
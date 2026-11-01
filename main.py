from sqlalchemy.exc import OperationalError

from controller import Controller
from database import make_engine, make_session_factory
from model import TaskModel
from repository import SqlAlchemyTaskRepository
from view import ConsoleView


def main():
    try:
        session_factory = make_session_factory(make_engine())
    except OperationalError:
        print("Не вдалося підключитися до бази даних. Перевір чи запущений docker compose up -d")
        return
    repository = SqlAlchemyTaskRepository(session_factory)
    Controller(TaskModel(repository), ConsoleView()).run()


if __name__ == "__main__":
    main()
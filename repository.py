from abc import ABC, abstractmethod

from sqlalchemy import select

from model import Task


class TaskRepository(ABC):
    @abstractmethod
    def add(self, task):
        pass

    @abstractmethod
    def get(self, task_id):
        pass

    @abstractmethod
    def list_all(self):
        pass

    @abstractmethod
    def list_by_status(self, status):
        pass

    @abstractmethod
    def update(self, task_id, description=None, schedule_for=None, status=None):
        pass

    @abstractmethod
    def delete(self, task_id):
        pass


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def add(self, task):
        with self.session_factory() as session:
            session.add(task)
            session.commit()
        return task

    def get(self, task_id):
        with self.session_factory() as session:
            return session.get(Task, task_id)

    def list_all(self):
        with self.session_factory() as session:
            stmt = select(Task).order_by(Task.created_at)
            return list(session.scalars(stmt).all())

    def list_by_status(self, status):
        with self.session_factory() as session:
            stmt = select(Task).where(Task.status == status).order_by(Task.created_at)
            return list(session.scalars(stmt).all())

    def update(self, task_id, description=None, schedule_for=None, status=None):
        with self.session_factory() as session:
            task = session.get(Task, task_id)
            if task is None:
                return None
            if description is not None:
                task.description = description
            if schedule_for is not None:
                task.schedule_for = schedule_for
            if status is not None:
                task.status = status
            session.commit()
            return task

    def delete(self, task_id):
        with self.session_factory() as session:
            task = session.get(Task, task_id)
            if task is None:
                return False
            session.delete(task)
            session.commit()
            return True
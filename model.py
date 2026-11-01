import enum
import uuid
from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Status(enum.Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class Task(Base):
    __tablename__ = "tasks"

    description: Mapped[str] = mapped_column(String(255))
    schedule_for: Mapped[datetime] = mapped_column()
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default_factory=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.now)
    status: Mapped[Status] = mapped_column(default=Status.TODO)


class TaskModel:
    def __init__(self, repository):
        self.repository = repository

    def add(self, description, schedule_for):
        description = description.strip()
        if not description:
            raise ValueError("Опис не може бути порожнім")
        return self.repository.add(Task(description, schedule_for))

    def get(self, task_id):
        return self.repository.get(task_id)

    def find(self, id_str):
        id_str = id_str.strip().lower()
        if not id_str:
            return None
        matches = [t for t in self.repository.list_all() if str(t.id).startswith(id_str)]
        if len(matches) == 1:
            return matches[0]
        return None

    def set_status(self, task_id, status):
        return self.repository.update(task_id, status=status)

    def update(self, task_id, description=None, schedule_for=None):
        if description is not None:
            description = description.strip()
            if not description:
                raise ValueError("Опис не може бути порожнім")
        return self.repository.update(task_id, description=description, schedule_for=schedule_for)

    def delete(self, task_id):
        return self.repository.delete(task_id)

    def all(self):
        return self.repository.list_all()

    def by_status(self, status):
        return self.repository.list_by_status(status)
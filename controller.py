from datetime import datetime
from model import Status
from view import DATE_FORMAT

STATUS_CHOICES = {
    "1": Status.TODO,
    "2": Status.IN_PROGRESS,
    "3": Status.DONE,
}


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.actions = {
            "1": self.create_task,
            "2": self.change_status,
            "3": self.delete_task,
            "4": self.edit_task,
            "5": self.list_tasks,
            "6": self.filter_tasks,
            "7": self.show_task,
        }

    def run(self):
        while True:
            self.view.show_menu()
            choice = self.view.ask("Ваш вибір: ")
            if choice == "0":
                self.view.show_message("До побачення")
                break
            action = self.actions.get(choice)
            if action is None:
                self.view.show_message("Невірний пункт меню")
                continue
            action()

    def read_date(self, text, allow_empty=False):
        while True:
            value = self.view.ask(text)
            if allow_empty and value == "":
                return None
            try:
                return datetime.strptime(value, DATE_FORMAT)
            except ValueError:
                self.view.show_message("Невірний формат, треба ДД.ММ.РРРР ГГ:ХХ")

    def ask_task(self):
        id_str = self.view.ask("Введіть id (можна перші символи): ")
        task = self.model.find(id_str)
        if task is None:
            self.view.show_message("Завдання не знайдено")
        return task

    def create_task(self):
        description = self.view.ask("Опис: ")
        if not description:
            self.view.show_message("Опис не може бути порожнім")
            return
        schedule_for = self.read_date("Дата і час (ДД.ММ.РРРР ГГ:ХХ): ")
        task = self.model.add(description, schedule_for)
        self.view.show_message("Створено завдання " + str(task.id))

    def change_status(self):
        task = self.ask_task()
        if task is None:
            return
        choice = self.view.ask("1 - InProgress, 2 - Done: ")
        if choice == "1":
            self.model.set_status(task.id, Status.IN_PROGRESS)
        elif choice == "2":
            self.model.set_status(task.id, Status.DONE)
        else:
            self.view.show_message("Невірний вибір")
            return
        self.view.show_message("Статус змінено")

    def delete_task(self):
        task = self.ask_task()
        if task is None:
            return
        self.model.delete(task.id)
        self.view.show_message("Завдання видалено")

    def edit_task(self):
        task = self.ask_task()
        if task is None:
            return
        description = self.view.ask("Новий опис (Enter - залишити): ")
        if description == "":
            description = None
        schedule_for = self.read_date("Нова дата (Enter - залишити): ", allow_empty=True)
        self.model.update(task.id, description, schedule_for)
        self.view.show_message("Завдання змінено")

    def list_tasks(self):
        self.view.show_tasks(self.model.all())

    def filter_tasks(self):
        choice = self.view.ask("1 - ToDo, 2 - InProgress, 3 - Done: ")
        status = STATUS_CHOICES.get(choice)
        if status is None:
            self.view.show_message("Невірний вибір")
            return
        self.view.show_tasks(self.model.by_status(status))

    def show_task(self):
        task = self.ask_task()
        if task is None:
            return
        self.view.show_tasks([task])
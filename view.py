DATE_FORMAT = "%d.%m.%Y %H:%M"


class ConsoleView:
    def show_menu(self):
        print()
        print("===== ToDo list =====")
        print("1 - Створити завдання")
        print("2 - Змінити статус")
        print("3 - Видалити завдання")
        print("4 - Редагувати завдання")
        print("5 - Показати всі завдання")
        print("6 - Фільтр за статусом")
        print("7 - Показати завдання за id")
        print("0 - Вихід")

    def ask(self, text):
        return input(text).strip()

    def show_message(self, text):
        print(text)

    def show_tasks(self, tasks):
        if not tasks:
            print("Список порожній")
            return
        headers = ["ID", "Опис", "Створено", "Заплановано", "Статус"]
        rows = []
        for t in tasks:
            rows.append([
                str(t.id),
                t.description,
                t.created_at.strftime(DATE_FORMAT),
                t.schedule_for.strftime(DATE_FORMAT),
                t.status.value,
            ])
        widths = []
        for i in range(len(headers)):
            widths.append(max(len(headers[i]), max(len(r[i]) for r in rows)))
        print(" | ".join(h.ljust(w) for h, w in zip(headers, widths)))
        print("-+-".join("-" * w for w in widths))
        for r in rows:
            print(" | ".join(c.ljust(w) for c, w in zip(r, widths)))
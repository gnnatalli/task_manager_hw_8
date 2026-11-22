from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'apps.tasks'

    def ready(self):
        # Подключаем сигналы приложения tasks
        import apps.tasks.signals

        # ready() — специальный метод Django, который выполняется при загрузке приложения.
        # import apps.tasks.signals — загружает наш файл с сигналами, чтобы Django зарегистрировал обработчики.
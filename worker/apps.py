from django.apps import AppConfig


class WorkerConfig(AppConfig):
    name = 'worker'
    verbose_name = "人员管理"
    def ready(self):
        import worker.signals

from django.apps import AppConfig


class AlertConfig(AppConfig):
    name = 'rulemanager.alert'

    def ready(self):
        from .tools import check_alert
        sch = check_alert.Scheduler()
        sch.start()
        sch.delete()

        # sch.init_job()



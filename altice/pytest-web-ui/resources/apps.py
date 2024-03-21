import sys
from django.apps import AppConfig


class ResourcesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'resources'
    def ready(self):
        try:
            if('runserver' not in sys.argv):
                return super().ready()
            from .models import Testbed, TestScheduler
            Testbed.objects.filter(status=False).update(status=True)
        except:
            print("New db schema")
from django.apps import AppConfig


class CeleryBeatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celery_beat'

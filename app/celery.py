import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

app = Celery("app", includes=["pokemon.tasks"])
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.task_routes = {"pokemon.tasks.catch_pokemon": {"queue": "pokemon_task_queue"}}

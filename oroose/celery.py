import os

# from core.configuration import only_one
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oroose.settings")

app = Celery("oroose")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "schedule-live-stocks-five-hundred-ten-minutes": {
        "task": "bengaluru.tasks.schedule_live_stocks_five_hundred",
        "schedule": 300.0,  # schedule every 10 minutes
        "args": (),
    },
    "schedule-zero-five-hundred-two-minutes": {
        "task": "bengaluru.tasks.schedule_zero_five_hundred",
        "schedule": 60.0,  # schedule every 2 minutes
        "args": (),
    },
}

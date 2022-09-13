from celery import shared_task
from oroose.celery import app
from datetime import datetime


# @shared_task(name='adds')
@app.task
def add(value):
    print(f"i call bengaluru.task.add {value} {datetime.now().strftime('%d-%m-%Y')}")

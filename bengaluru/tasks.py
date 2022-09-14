from oroose.celery import app
from .evaluation import polling_live_stocks_five_hundred


@app.task
def schedule_live_stocks_five_hundred():
    print("Schedule live stocks five hundred started")
    polling_live_stocks_five_hundred()
    print("Schedule live stocks five hundred end")

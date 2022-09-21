from oroose.celery import app
from .evaluation import polling_live_stocks_five_hundred, analyse_stocks_five_hundred
from core.configuration import ConfigSettings


@app.task
def schedule_live_stocks_five_hundred():
    print("Schedule live stocks five hundred started")
    if ConfigSettings().get_conf("FH_LIVE_STOCKS_NSE"):
        print("Schedule live stocks five hundred in-progress")
        polling_live_stocks_five_hundred()
        print("Schedule live stocks five hundred zero in-progress")
        analyse_stocks_five_hundred()
    print("Schedule live stocks five hundred end")

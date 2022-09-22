from oroose.celery import app
from .evaluation import polling_live_stocks_five_hundred, analyse_stocks_five_hundred
from core.configuration import ConfigSettings
from core.models import DataLog
from datetime import datetime
from django.utils.timezone import get_current_timezone


@app.task
def schedule_live_stocks_five_hundred():
    print("Schedule live stocks five hundred started")
    data_log_name = ConfigSettings().get_conf("LOG_SCHEDULE_LIVE_500")
    obj = DataLog(
        date=datetime.now(),
        start_time=datetime.now().replace(tzinfo=get_current_timezone()),
        name=data_log_name,
    )
    obj.save()
    if ConfigSettings().get_conf("FH_LIVE_STOCKS_NSE"):
        print("Schedule live stocks five hundred in-progress")
        polling_live_stocks_five_hundred()
        print("Schedule live stocks five hundred zero in-progress")
        analyse_stocks_five_hundred()
    print("Schedule live stocks five hundred end")
    obj.end_time = datetime.now()
    obj.save()

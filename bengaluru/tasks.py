from datetime import datetime

from django.utils.timezone import get_current_timezone

from core.configuration import ParameterStore
from core.models import DataLog, ParameterSettings
from oroose.celery import app

from .evaluation import analyse_stocks_five_hundred, polling_live_stocks_five_hundred


LOG_SCHEDULE_LIVE_500 = ParameterStore().get_conf("LOG_SCHEDULE_LIVE_500")
SETTINGS_FH_LIVE_STOCKS_NSE = "SETTINGS_FH_LIVE_STOCKS_NSE"


def condition_schedule_live_stocks_fh():
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)
    if ps.status:
        return True
    return False


@app.task
def schedule_live_stocks_five_hundred():
    print("Schedule live stocks five hundred started")
    obj = DataLog(
        date=datetime.now(),
        start_time=datetime.now().replace(tzinfo=get_current_timezone()),
        name=LOG_SCHEDULE_LIVE_500,
    )
    obj.save()
    print(condition_schedule_live_stocks_fh())
    if condition_schedule_live_stocks_fh():
        print("Schedule live stocks five hundred in-progress")
        polling_live_stocks_five_hundred()
        print("Schedule live stocks five hundred zero in-progress")
        analyse_stocks_five_hundred()
    print("Schedule live stocks five hundred end")
    obj.end_time = datetime.now()
    obj.save()

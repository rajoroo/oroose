import logging
from datetime import datetime

from django.conf import settings

from core.configuration import only_one
from core.models import DataLog, ParameterSettings
from oroose.celery import app

from .stock_monitor import polling_live_stocks_five_hundred
from .up_trend import trigger_fhz_uptrend, process_fhz_uptrend
from .down_trend import trigger_fhz_downtrend, process_fhz_downtrend

logger = logging.getLogger("celery")


LOG_SCHEDULE_LIVE_500 = settings.LOG_SCHEDULE_LIVE_500
LOG_SCHEDULE_ZERO_500 = settings.LOG_SCHEDULE_ZERO_500
FH_STOCK_LIVE_START = settings.FH_STOCK_LIVE_START
FH_STOCK_LIVE_END = settings.FH_STOCK_LIVE_END
FH_ZERO_START = settings.FH_ZERO_START
FH_ZERO_END = settings.FH_ZERO_END

SETTINGS_FH_LIVE_STOCKS_NSE = "SETTINGS_FH_LIVE_STOCKS_NSE"
SETTINGS_FH_ZERO = "SETTINGS_FH_ZERO"


def condition_schedule_live_stocks_fh():
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)
    start = datetime.strptime(FH_STOCK_LIVE_START, "%H%M").time()
    end = datetime.strptime(FH_STOCK_LIVE_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)

    if ps.status and (start_time <= datetime.now() <= end_time) and (datetime.today().weekday() < 5):
        return True

    return False


@app.task(name="bengaluru.tasks.schedule_live_stocks_five_hundred")
@only_one(key="SingleTask", timeout=60 * 15)
def schedule_live_stocks_five_hundred():
    logger.info("FH Started")
    obj = DataLog(
        date=datetime.now(),
        start_time=datetime.now(),
        name=LOG_SCHEDULE_LIVE_500,
    )
    obj.save()
    if condition_schedule_live_stocks_fh():
        polling_live_stocks_five_hundred()
        trigger_fhz_uptrend()
        trigger_fhz_downtrend()
    logger.info("FH end")
    obj.end_time = datetime.now()
    obj.save()


def condition_schedule_zero_fh():
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_ZERO)
    start = datetime.strptime(FH_ZERO_START, "%H%M").time()
    end = datetime.strptime(FH_ZERO_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)

    if ps.status and (start_time <= datetime.now() <= end_time) and (datetime.today().weekday() < 5):
        return True

    return False


@app.task(name="bengaluru.tasks.schedule_fhz_uptrend")
@only_one(key="SingleTask", timeout=60 * 5)
def schedule_fhz_uptrend():
    logger.info("ZERO uptrend started")
    obj = DataLog(
        date=datetime.now(),
        start_time=datetime.now(),
        name=LOG_SCHEDULE_ZERO_500,
    )
    obj.save()
    if condition_schedule_zero_fh():
        process_fhz_uptrend()
    logger.info("ZERO uptrend end")
    obj.end_time = datetime.now()
    obj.save()


@app.task(name="bengaluru.tasks.schedule_fhz_downtrend")
@only_one(key="SingleTask", timeout=60 * 5)
def schedule_fhz_downtrend():
    logger.info("ZERO downtrend started")
    obj = DataLog(
        date=datetime.now(),
        start_time=datetime.now(),
        name=LOG_SCHEDULE_ZERO_500,
    )
    obj.save()
    if condition_schedule_zero_fh():
        process_fhz_downtrend()
    logger.info("ZERO downtrend end")
    obj.end_time = datetime.now()
    obj.save()

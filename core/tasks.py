import logging
from datetime import datetime

from core.configuration import only_one
from core.models import DataLog, ParameterSettings
from oroose.celery import app

from stockwatch.stock_monitor import polling_live_stocks_five_hundred
from bengaluru.up_trend import trigger_fhz_uptrend, process_fhz_uptrend
from mysuru.down_trend import trigger_fhz_downtrend, process_fhz_downtrend
from core.constant import (
    SETTINGS_FH_LIVE_STOCKS_NSE,
    SETTINGS_FHZ_UPTREND,
    SETTINGS_FHZ_DOWNTREND,
    LOG_SCHEDULE_LIVE_500,
    LOG_SCHEDULE_ZERO_500,
)
from stockwatch.constant import LIVE_START, LIVE_END
from bengaluru.constant import BENGALURU_START, BENGALURU_END
from mysuru.constant import MYSURU_START, MYSURU_END

logger = logging.getLogger("celery")


def condition_schedule_live_stocks_fh():
    print("i call")
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)
    start = datetime.strptime(LIVE_START, "%H%M").time()
    end = datetime.strptime(LIVE_END, "%H%M").time()
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


def condition_schedule_fhz_uptrend():
    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_UPTREND)
    start = datetime.strptime(BENGALURU_START, "%H%M").time()
    end = datetime.strptime(BENGALURU_END, "%H%M").time()
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
    if condition_schedule_fhz_uptrend():
        process_fhz_uptrend()
    logger.info("ZERO uptrend end")
    obj.end_time = datetime.now()
    obj.save()


def condition_schedule_fhz_downtrend():
    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_DOWNTREND)
    start = datetime.strptime(MYSURU_START, "%H%M").time()
    end = datetime.strptime(MYSURU_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)

    if ps.status and (start_time <= datetime.now() <= end_time) and (datetime.today().weekday() < 5):
        return True

    return False


@app.task(name="bengaluru.tasks.schedule_fhz_downtrend")
@only_one(key="SecondTask", timeout=60 * 5)
def schedule_fhz_downtrend():
    print("Down trend started-----------")
    logger.info("ZERO downtrend started")
    obj = DataLog(
        date=datetime.now(),
        start_time=datetime.now(),
        name=LOG_SCHEDULE_ZERO_500,
    )
    obj.save()
    if condition_schedule_fhz_downtrend():
        process_fhz_downtrend()
    logger.info("ZERO downtrend end")
    obj.end_time = datetime.now()
    obj.save()

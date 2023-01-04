import logging
from datetime import datetime

from bengaluru.constant import BENGALURU_END, BENGALURU_START
from bengaluru.up_trend import process_fhz_uptrend, trigger_fhz_uptrend
from core.configuration import only_one
from core.constant import (
    LOG_SCHEDULE_LIVE_500,
    LOG_SCHEDULE_ZERO_500,
    SETTINGS_FH_LIVE_STOCKS_NSE,
    SETTINGS_FHZ_DOWNTREND,
    SETTINGS_FHZ_UPTREND,
)
from core.models import DataLog, ParameterSettings
from mysuru.constant import MYSURU_END, MYSURU_START
from mysuru.down_trend import process_fhz_downtrend, trigger_fhz_downtrend
from oroose.celery import app
from stockwatch.constant import FIVEHUNDRED_END, FIVEHUNDRED_START, LIVE_END, LIVE_START
from stockwatch.stock_monitor import polling_live_stocks_five_hundred, polling_stocks

logger = logging.getLogger("celery")


def condition_schedule_live_stocks_fh():
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)
    start = datetime.strptime(LIVE_START, "%H%M").time()
    end = datetime.strptime(LIVE_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)

    if ps.status and (start_time <= datetime.now() <= end_time) and (datetime.today().weekday() < 5):
        return True

    return False


def condition_schedule_fh_stocks():
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_LIVE_STOCKS_NSE)
    start = datetime.strptime(FIVEHUNDRED_START, "%H%M").time()
    end = datetime.strptime(FIVEHUNDRED_END, "%H%M").time()
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

    if condition_schedule_fh_stocks():
        polling_stocks()
        # trigger_fhz_uptrend()
        trigger_fhz_downtrend()

    print("*********************************************")
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

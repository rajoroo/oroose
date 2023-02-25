import logging
from datetime import datetime

from bengaluru.up_trend import process_fhz_uptrend, generate_bengaluru, maintain_bengaluru
from core.configuration import only_one
from core.constant import (
    LOG_SCHEDULE_LIVE_500,
    LOG_SCHEDULE_ZERO_500,
)
from core.models import DataLog
from core.tools import get_param_config_tag, get_today_datetime
from oroose.celery import app
from stockwatch.stock_monitor import polling_live_stocks_five_hundred, polling_stocks

logger = logging.getLogger("celery")


def condition_schedule_live_stocks_fh():
    config = get_param_config_tag(tag="LIVE")
    start_time = get_today_datetime(time_str=config.get("start_time"))
    end_time = get_today_datetime(time_str=config.get("end_time"))

    if (
        config.get("live_status")
        and (start_time <= datetime.now() <= end_time)
        and (datetime.today().weekday() < 5)
    ):
        return True

    return False


def condition_schedule_bengaluru():
    config = get_param_config_tag(tag="BENGALURU")
    start_time = get_today_datetime(time_str=config.get("start_time"))
    end_time = get_today_datetime(time_str=config.get("end_time"))

    if (
        config.get("bengaluru_status")
        and (start_time <= datetime.now() <= end_time)
        and (datetime.today().weekday() < 5)
    ):
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

    # Poll and create stock
    if condition_schedule_live_stocks_fh():
        polling_live_stocks_five_hundred()
        polling_stocks()

    if condition_schedule_bengaluru():
        generate_bengaluru()
        maintain_bengaluru()

    print("*********************************************")
    logger.info("FH end")
    obj.end_time = datetime.now()
    obj.save()


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
    if condition_schedule_bengaluru():
        process_fhz_uptrend()
    logger.info("ZERO uptrend end")
    obj.end_time = datetime.now()
    obj.save()

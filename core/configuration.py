import redis
from django.conf import settings

from bengaluru.constant import BENGALURU_CONFIGURATION, BENGALURU_END, BENGALURU_START
from core.constant import LOG_SCHEDULE_LIVE_500, LOG_SCHEDULE_ZERO_500
from stockwatch.constant import FIVEHUNDRED_END, FIVEHUNDRED_START, LIVE_END, LIVE_START

REDIS_CLIENT = redis.Redis.from_url(settings.CELERY_BROKER_URL)


parameter_store = {
    "api": {
        "display_name": "API",
        "value": {
            "LIVE_INDEX_URL": settings.LIVE_INDEX_URL,
            "LIVE_INDEX_500_URL": settings.LIVE_INDEX_500_URL,
        },
    },
    "five_hundred_uptrend": BENGALURU_CONFIGURATION,
    "timings": {
        "display_name": "Timings",
        "value": {
            "LIVE_START": LIVE_START,
            "LIVE_END": LIVE_END,
            "FIVEHUNDRED_START": FIVEHUNDRED_START,
            "FIVEHUNDRED_END": FIVEHUNDRED_END,
            "BENGALURU_START": BENGALURU_START,
            "BENGALURU_END": BENGALURU_END,
        },
    },
    "loggers": {
        "display_name": "Loggers",
        "value": {
            "LOG_SCHEDULE_LIVE_500": LOG_SCHEDULE_LIVE_500,
            "LOG_SCHEDULE_ZERO_500": LOG_SCHEDULE_ZERO_500,
        },
    },
}


def only_one(function=None, key="", timeout=None):
    """Enforce only one celery task at a time."""

    def _dec(run_func):
        """Decorator."""

        def _caller(*args, **kwargs):
            """Caller."""
            ret_value = None
            have_lock = False
            lock = REDIS_CLIENT.lock(key, timeout=timeout)
            try:
                have_lock = lock.acquire(blocking=False)
                if have_lock:
                    ret_value = run_func(*args, **kwargs)
            finally:
                if have_lock:
                    lock.release()

            return ret_value

        return _caller

    return _dec(function) if function is not None else _dec

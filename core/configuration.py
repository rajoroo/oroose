import json
import redis

from django.conf import settings

REDIS_CLIENT = redis.Redis()


parameter_store = {
    "api": {
        "display_name": "API",
        "value": {
            "LIVE_INDEX_URL": settings.LIVE_INDEX_URL,
            "LIVE_INDEX_500_URL": settings.LIVE_INDEX_500_URL,
        }

    },
    "five_hundred": {
        "display_name": "Five Hundred",
        "value": {
            "FH_RANK_FROM": settings.FH_RANK_FROM,
            "FH_RANK_TILL": settings.FH_RANK_TILL,
            "FH_MAX_PRICE": settings.FH_MAX_PRICE,
            "FH_MAX_PERCENT": settings.FH_MAX_PERCENT,
            "FH_MAX_BUY_ORDER": settings.FH_MAX_BUY_ORDER,
        }

    },
    "timings": {
        "display_name": "Timings",
        "value": {
            "FH_STOCK_LIVE_START": settings.FH_STOCK_LIVE_START,
            "FH_STOCK_LIVE_END": settings.FH_STOCK_LIVE_END,
            "FH_ZERO_START": settings.FH_ZERO_START,
            "FH_ZERO_END": settings.FH_ZERO_END,
        }

    },
    "loggers": {
        "display_name": "Loggers",
        "value": {
            "LOG_SCHEDULE_LIVE_500": settings.LOG_SCHEDULE_LIVE_500,
            "LOG_SCHEDULE_ZERO_500": settings.LOG_SCHEDULE_ZERO_500,
        }

    },
}


class ParameterStore:
    def __init__(self):
        self.path = settings.LOAD_CONFIG_PATH
        self.data = None

    def load_data(self):
        json_file = open(self.path)
        config_data = json.load(json_file)
        self.data = config_data["data"]
        return True

    def get_all_configs(self, prefix=None):
        self.load_data()
        if prefix:
            return {k: v for k, v in self.data.items() if k.startswith(prefix)}

        return self.data

    def get_conf(self, name):
        self.load_data()
        return self.data.get(name, None)


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

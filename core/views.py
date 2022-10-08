import json
import sys

from django.conf import settings


def pre_check_server_start():
    with open(settings.LOAD_CONFIG_PATH) as json_file:
        config_data = json.load(json_file)

    confs = config_data["data"]
    conf = list(confs.keys())

    items = [
        # API control
        "SETTINGS_FH_LIVE_STOCKS_NSE",
        "SETTINGS_FH_ZERO",

        # API
        "LIVE_INDEX_URL",
        "LIVE_INDEX_500_URL",

        # FHZ Configuration
        "FH_RANK_FROM",
        "FH_RANK_TILL",
        "FH_MAX_PRICE",
        "FH_MAX_PERCENT",
        "FH_MAX_BUY_ORDER",
        "FH_STOCK_LIVE_START",
        "FH_STOCK_LIVE_END",

        # Logger
        "LOG_SCHEDULE_LIVE_500",
        "LOG_SCHEDULE_ZERO_500",

        # Timing
        "FH_ZERO_START",
        "FH_ZERO_END",
    ]

    conf_not_exist = ', '.join([item for item in items if item not in conf])
    if conf_not_exist:
        print(f"Please check config json file keys - {conf_not_exist}")
        sys.exit(1)

    return True

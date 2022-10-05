import json
import sys

from django.conf import settings


def pre_check_server_start():
    json_file = open(settings.LOAD_CONFIG_PATH)
    config_data = json.load(json_file)

    confs = config_data["data"]
    conf = list(confs.keys())

    items = [
        "SETTINGS_FH_LIVE_STOCKS_NSE",
        "SETTINGS_FH_ZERO",
        "LIVE_INDEX_URL",
        "LIVE_INDEX_500_URL",
        "FH_RANK_FROM",
        "FH_RANK_TILL",
        "FH_MAX_PRICE",
        "FH_MAX_PERCENT",
        "FH_MAX_BUY_ORDER",
        "FH_STOCK_LIVE_START",
        "FH_STOCK_LIVE_END",
        "LOG_SCHEDULE_LIVE_500",
        "LOG_SCHEDULE_ZERO_500",
        "FH_ZERO_START",
        "FH_ZERO_END",
    ]

    for item in items:
        if item not in conf:
            print("Please check config json file.")
            sys.exit(1)

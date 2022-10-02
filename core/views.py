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
        "LIVE_INDEX_URL",
        "LIVE_INDEX_500_URL",
    ]

    for item in items:
        if item not in conf:
            print("Please check config json file.")
            sys.exit(1)

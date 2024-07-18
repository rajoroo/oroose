from mysuru.fetch_trend import FetchTrend
from datetime import datetime


def trading_m5_fetch(name):
    """
    Fetch data form the API
    Parameters:
        name - model name string representation
    """
    trend_obj = FetchTrend()
    trend_obj.fetch_trading_value(name)

    print(f"================I fetch - {datetime.now()}=================")
    trend_obj.raise_alert_message()
    return True


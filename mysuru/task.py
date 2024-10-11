from core.telegram_util import TelegramAlert
from mysuru.fetch_trend import FetchTrend
from datetime import datetime
from mysuru.models import StockData


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

def trading_m15_sensitive_fetch(name):
    trend_obj = FetchTrend()
    trend_obj.fetch_trading_value(name)
    recs = StockData.objects.filter(is_trading=True, trading_status="up")
    for rec in recs:
        if rec.m15_ha_close_0 > rec.m15_ha_open_0:
            print(f"EMA: {rec.m15_ema_20_0} Close: {rec.m15_ha_close_0} Green")
        else:
            print(f"EMA: {rec.m15_ema_20_0} Close: {rec.m15_ha_close_0} Red")
            TelegramAlert.send_message(rec.symbol)

    # Down Values
    recs = StockData.objects.filter(is_trading=True, trading_status="dn")
    for rec in recs:
        if rec.m15_ha_close_0 > rec.m15_ha_open_0:
            print(f"EMA: {rec.m15_ema_20_0} Close: {rec.m15_ha_close_0} Green")
            TelegramAlert.send_message(rec.symbol)
        else:
            print(f"EMA: {rec.m15_ema_20_0} Close: {rec.m15_ha_close_0} Red")


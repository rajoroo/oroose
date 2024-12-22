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


def trading_m5_sensitive_fetch(name):
    trend_obj = FetchTrend()
    trend_obj.fetch_trading_value(name)
    recs = StockData.objects.filter(is_trading=True, trading_status="up")
    for rec in recs:
        if rec.m5_ema_5_0 > rec.m5_ema_20_0:
            print(
                f"EMA 5: {rec.m5_ema_5_0} EMA 20: {rec.m5_ema_5_0} EMA 50: {rec.m5_ema_50_0} Close: {rec.m5_ha_close_0} Green"
            )
        else:
            message = f"SYMBOL:{rec.symbol} EMA 5: {rec.m5_ema_5_0} EMA 20: {rec.m5_ema_5_0} EMA 50: {rec.m5_ema_50_0} Close: {rec.m5_ha_close_0} Red"
            print(message)
            TelegramAlert.send_message(message)

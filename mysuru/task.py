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
        rsi_value = getattr(rec, f"{name}_rsi_0")
        reverse_rsi_value = getattr(rec, f"{name}_rev_rsi")
        message = f"SYMBOL:{rec.symbol} -- {name} RSI:{rsi_value} -- {name} Reverse RSI: {reverse_rsi_value}"
        print(message)
        if rsi_value < 50:
            TelegramAlert.send_message(message)

    recs = StockData.objects.filter(is_trading=True, trading_status="dn")
    for rec in recs:
        rsi_value = getattr(rec, f"{name}_rsi_0")
        reverse_rsi_value = getattr(rec, f"{name}_rev_rsi")
        message = f"SYMBOL:{rec.symbol} -- {name} RSI:{rsi_value} -- {name} Reverse RSI: {reverse_rsi_value}"
        print(message)
        if rsi_value > 50:
            TelegramAlert.send_message(message)

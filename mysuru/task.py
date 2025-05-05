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
        reverse_rsi_value = getattr(rec, f"{name}_rev_rsi_50")
        message = f"SYMBOL:{rec.symbol} -- {name} RSI:{rsi_value} -- {name} Reverse RSI: {reverse_rsi_value}"
        print(message)
        if rsi_value < 50:
            TelegramAlert.send_message(message)

    recs = StockData.objects.filter(is_trading=True, trading_status="dn")
    for rec in recs:
        rsi_value = getattr(rec, f"{name}_rsi_0")
        reverse_rsi_value = getattr(rec, f"{name}_rev_rsi_50")
        message = f"SYMBOL:{rec.symbol} -- {name} RSI:{rsi_value} -- {name} Reverse RSI: {reverse_rsi_value}"
        print(message)
        if rsi_value > 50:
            TelegramAlert.send_message(message)


def trading_day_sensitive_fetch(name):
    trend_obj = FetchTrend()
    trend_obj.fetch_trading_value(name)
    recs = StockData.objects.filter(is_trading=True, trading_status="up")
    for rec in recs:
        message_list = [f"SYMBOL:{rec.symbol} "]
        if (rec.day_rsi_1 > 60) and (rec.day_rsi_0 < 60):
            message_list.append(f"-- Day RSI below 60:{rec.day_rsi_0}")

        if rec.day_ha_open_0 > rec.day_ha_close_0:
            message_list.append(f"-- Day HA RED:{rec.day_ha_open_0}")

        if rec.day_close_0 < rec.day_ema_20_0:
            message_list.append(f"-- Day close below 20 SMA:{rec.day_close_0}")

        message = ", ".join(message_list)
        print(message)
        if len(message_list) > 1:
            TelegramAlert.send_message(message)

    recs = StockData.objects.filter(is_trading=True, trading_status="dn")
    for rec in recs:
        message_list = [f"SYMBOL:{rec.symbol} "]
        if rec.day_ha_close_0 > rec.day_ha_open_0:
            message_list.append(f"-- Day HA Green:{rec.day_ha_open_0}")

        if (rec.day_close_0 > rec.day_ema_20_0) and (rec.day_close_1 < rec.day_ema_20_0):
            message_list.append(f"-- Day close above 20 SMA:{rec.day_close_0}")

        message = ", ".join(message_list)
        print(message)
        if len(message_list) > 1:
            TelegramAlert.send_message(message)

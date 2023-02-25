import logging
from datetime import datetime

from django.conf import settings

from stockwatch.choice import SignalStatus
from stockwatch.models import FiveHundred, StockWatchFh
from stockwatch.stocks import LiveStocks

logger = logging.getLogger("celery")


def update_five_hundred(data):
    for key, value in data.items():
        items = FiveHundred.objects.filter(date=datetime.today(), symbol=value["symbol"])
        if items:
            obj = items[0]
            obj.rank = value["rank"]
            obj.last_price = value["last_price"]
            obj.percentage_change = value["percentage_change"]
            obj.save()
            obj.get_signal_status()
        else:
            fh = FiveHundred.objects.create(
                date=datetime.today(),
                created_date=datetime.now(),
                symbol=value["symbol"],
                identifier=value["identifier"],
                isin=value["isin"],
                company_name=value["company_name"],
                rank=value["rank"],
                last_price=value["last_price"],
                percentage_change=value["percentage_change"],
                signal_status=SignalStatus.INPROG,
            )
            fh.is_valid_stock()
            fh.get_smart_token()
            # fh.get_ksec_token()
            fh.get_signal_status()

    return True


def update_stock_watch_fh(data):

    stock_data = {
        row["symbol"]: {
            "date": datetime.today().strftime("%d-%b-%Y"),
            "time": row["lastUpdateTime"],
            "symbol": row["symbol"],
            "identifier": row["identifier"],
            "last_price": row["lastPrice"],
            "percentage_change": row["pChange"],
            "isin": row["meta.isin"],
            "company_name": row["meta.companyName"],
            "rank": row["index"],
        }
        for index, row in data.iterrows()
    }

    StockWatchFh.objects.create(
        date=datetime.today(),
        created_date=datetime.now(),
        stock_data=stock_data,
    )
    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list("symbol", flat=True)
    try:
        obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL, symbols=symbols)

        # Get live data, feed data, save data
        obj.get_live_data()
        obj.save_stock_data()
        # obj.get_feed_data()

        # Raw data
        df = obj.get_live_stock_list()
        update_stock_watch_fh(data=df)
    except:
        logger.info(f"Live stock NSE not working")

    return True


def polling_stocks():
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list("symbol", flat=True)
    obj = StockWatchFh.objects.all().order_by("-id").first()
    if (not obj) and (not hasattr(obj, "stock_data")):
        return False

    stocks = {key: value for key, value in obj.stock_data.items() if (value["rank"] <= 5) or (key in symbols)}
    update_five_hundred(data=stocks)
    return True

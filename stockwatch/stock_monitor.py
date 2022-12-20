from datetime import datetime

from stockwatch.models import FiveHundred, StockWatchFh
from stockwatch.stocks import LiveStocks
from stockwatch.choice import SignalStatus
from django.conf import settings


def update_five_hundred(data):
    for key, value in data.items():
        items = FiveHundred.objects.filter(date=datetime.now(), symbol=value["symbol"])
        time_obj = datetime.strptime(value["time"], "%d-%b-%Y %H:%M:%S")
        if items:
            obj = items[0]
            obj.date = datetime.today()
            obj.time = time_obj
            obj.previous_rank = obj.rank if value["rank"] != obj.rank else obj.previous_rank
            obj.rank = value["rank"]
            obj.last_price = value["last_price"]
            obj.percentage_change = value["percentage_change"]
            obj.highest_rank = value["rank"] if value["rank"] < obj.highest_rank else obj.highest_rank
            obj.lowest_rank = value["rank"] if value["rank"] > obj.lowest_rank else obj.lowest_rank
            obj.previous_price = obj.last_price
            obj.previous_price_20min = obj.get_previous_20_min(time_obj=time_obj)
            obj.signal_status = obj.get_signal_status(time_obj=time_obj, price=value["last_price"])
            obj.save()
        else:
            FiveHundred.objects.create(
                date=datetime.today(),
                time=time_obj,
                created_date=datetime.now(),
                symbol=value["symbol"],
                identifier=value["identifier"],
                last_price=value["last_price"],
                previous_price=value["last_price"],
                percentage_change=value["percentage_change"],
                isin=value["isin"],
                company_name=value["company_name"],
                rank=value["rank"],
                highest_rank=value["rank"],
                lowest_rank=value["rank"],
                previous_rank=value["rank"],
                signal_status=SignalStatus.INPROG,
            )

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
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL, symbols=symbols)

    # Get live data, feed data, save data
    obj.get_live_data()
    # obj.get_feed_data()
    obj.save_stock_data()

    # Bengaluru/ Mysuru
    # df_1 = obj.filter_stock_list()
    # update_five_hundred(data=df_1)

    # Raw data
    df_2 = obj.get_live_stock_list()
    update_stock_watch_fh(data=df_2)
    return True


def polling_stocks():
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list("symbol", flat=True)
    obj = StockWatchFh.objects.all().order_by("-id").first()
    if (not obj) and (not hasattr(obj, 'stock_data')):
        return False

    stocks = {
        key: value
        for key, value in obj.stock_data.items()
        if (value["rank"] <= 5) or (key in symbols)
    }
    update_five_hundred(data=stocks)
    return True




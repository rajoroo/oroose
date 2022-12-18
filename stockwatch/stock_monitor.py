from datetime import datetime

from stockwatch.models import FiveHundred, StockWatchFh
from stockwatch.stocks import LiveStocks
from django.conf import settings
from django.db.models import Max


def update_five_hundred(data):
    for index, row in data.iterrows():
        items = FiveHundred.objects.filter(date=datetime.now(), symbol=row["symbol"])
        if items:
            obj = items[0]
            obj.date = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S")
            obj.time = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S")
            obj.previous_rank = obj.rank if row["index"] != obj.rank else obj.previous_rank
            obj.rank = row["index"]
            obj.last_price = row["lastPrice"]
            obj.percentage_change = row["pChange"]
            obj.highest_rank = row["index"] if row["index"] < obj.highest_rank else obj.highest_rank
            obj.lowest_rank = row["index"] if row["index"] > obj.lowest_rank else obj.lowest_rank
            obj.previous_price = obj.last_price if row["index"] != obj.rank else obj.previous_price
            obj.save()
        else:
            obj = FiveHundred(
                date=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
                time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
                created_date=datetime.now(),
                symbol=row["symbol"],
                identifier=row["identifier"],
                last_price=row["lastPrice"],
                previous_price=row["lastPrice"],
                percentage_change=row["pChange"],
                isin=row["meta.isin"],
                company_name=row["meta.companyName"],
                rank=row["index"],
                highest_rank=row["index"],
                lowest_rank=row["index"],
                previous_rank=row["index"],
                bar="level0",
            )
            obj.save()

    return True


def update_stock_watch_fh(data):
    uid = 1
    last_uid = StockWatchFh.objects.aggregate(Max('uid'))["uid__max"]
    if last_uid:
        uid = last_uid + 1

    stock_object = [
        StockWatchFh(
            uid=uid,
            date=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
            time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
            created_date=datetime.now(),
            symbol=row["symbol"],
            identifier=row["identifier"],
            last_price=row["lastPrice"],
            percentage_change=row["pChange"],
            isin=row["meta.isin"],
            company_name=row["meta.companyName"],
            rank=row["index"],
        )
        for index, row in data.iterrows()
    ]

    StockWatchFh.objects.bulk_create(stock_object)
    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list("symbol", flat=True)
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL, symbols=symbols)
    # obj.get_live_data()
    obj.get_feed_data()
    # obj.save_stock_data()

    # Bengaluru/ Mysuru
    df_1 = obj.filter_stock_list()
    update_five_hundred(data=df_1)

    # Raw data
    df_2 = obj.get_live_stock_list()
    update_stock_watch_fh(data=df_2)
    return True

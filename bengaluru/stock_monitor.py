from datetime import datetime

from django.conf import settings

from bengaluru.models import FiveHundred
from core.stocks import LiveStocks

LIVE_INDEX_URL = settings.LIVE_INDEX_URL
LIVE_INDEX_500_URL = settings.LIVE_INDEX_500_URL
FH_MAX_TOTAL_PRICE = settings.FH_MAX_TOTAL_PRICE  # 20000


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

            obj.save()
        else:
            obj = FiveHundred(
                date=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
                time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
                symbol=row["symbol"],
                identifier=row["identifier"],
                last_price=row["lastPrice"],
                percentage_change=row["pChange"],
                isin=row["meta.isin"],
                company_name=row["meta.companyName"],
                rank=row["index"],
                highest_rank=row["index"],
                lowest_rank=row["index"],
                previous_rank=row["index"],
            )
            obj.save()

    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list("symbol", flat=True)
    obj = LiveStocks(base_url=LIVE_INDEX_URL, url=LIVE_INDEX_500_URL, symbols=symbols)
    df = obj.filter_stock_list()
    return update_five_hundred(data=df)

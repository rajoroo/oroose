from bengaluru.models import FiveHundred
from datetime import datetime
from core.stocks import LiveStocks
from django.conf import settings


def update_five_hundred(data):
    FiveHundred.objects.filter(date=datetime.now()).update(rank=None)

    for index, row in data.iterrows():
        items = FiveHundred.objects.filter(date=datetime.now(), symbol=row["symbol"])
        if items:
            obj = items[0]
            obj.time = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S")
            obj.rank = index
            obj.last_price = row["lastPrice"]
            obj.percentage_change = row["pChange"]
            obj.save()
        else:
            obj = FiveHundred(
                date=datetime.now(),
                symbol=row["symbol"],
                identifier=row["identifier"],
                last_price=row["lastPrice"],
                percentage_change=row["pChange"],
                isin=row["meta.isin"],
                company_name=row["meta.companyName"],
                time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S"),
                rank=index,
            )
            obj.save()
    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL)
    df = obj.filter_stock_list()
    return update_five_hundred(data=df)

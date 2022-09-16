from bengaluru.models import FiveHundred, FiveHundredStatus
from datetime import datetime
from core.stocks import LiveStocks
from django.conf import settings
from django.utils.timezone import get_current_timezone


def update_five_hundred(data):
    FiveHundred.objects.filter(date=datetime.now()).update(rank=None)

    for index, row in data.iterrows():
        items = FiveHundred.objects.filter(date=datetime.now(), symbol=row["symbol"])
        if items:
            obj = items[0]
            obj.date = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(tzinfo=get_current_timezone())
            obj.time = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(tzinfo=get_current_timezone())
            obj.rank = row['index']
            obj.last_price = row["lastPrice"]
            obj.percentage_change = row["pChange"]
            obj.status = FiveHundredStatus.TOPPER if row['index'] <= 5 else FiveHundredStatus.BOTTOM
            obj.save()
        else:
            obj = FiveHundred(
                date=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(tzinfo=get_current_timezone()),
                symbol=row["symbol"],
                identifier=row["identifier"],
                last_price=row["lastPrice"],
                percentage_change=row["pChange"],
                isin=row["meta.isin"],
                company_name=row["meta.companyName"],
                time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(tzinfo=get_current_timezone()),
                rank=row['index'],
                status=FiveHundredStatus.TOPPER if row['index'] <= 5 else FiveHundredStatus.BOTTOM
            )
            obj.save()

    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list('symbol', flat=True)
    obj = LiveStocks(
        base_url=settings.LIVE_INDEX_URL,
        url=settings.LIVE_INDEX_500_URL,
        symbols=symbols
    )
    # df = obj.filter_stock_list()
    df = obj.filter_stock_list_v1()
    return update_five_hundred(data=df)

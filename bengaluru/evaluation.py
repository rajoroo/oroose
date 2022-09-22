from bengaluru.models import FiveHundred, FhZero, FhZeroStatus
from datetime import datetime
from core.stocks import LiveStocks
from django.utils.timezone import get_current_timezone
from core.configuration import ConfigSettings


def update_five_hundred(data):
    FiveHundred.objects.filter(date=datetime.now()).update(rank=None)

    for index, row in data.iterrows():
        items = FiveHundred.objects.filter(date=datetime.now(), symbol=row["symbol"])
        if items:
            obj = items[0]
            obj.date = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                tzinfo=get_current_timezone())
            obj.time = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                tzinfo=get_current_timezone())
            obj.rank = row['index']
            obj.last_price = row["lastPrice"]
            obj.percentage_change = row["pChange"]
            obj.save()
        else:
            obj = FiveHundred(
                date=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                    tzinfo=get_current_timezone()),
                time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                    tzinfo=get_current_timezone()),
                symbol=row["symbol"],
                identifier=row["identifier"],
                last_price=row["lastPrice"],
                percentage_change=row["pChange"],
                isin=row["meta.isin"],
                company_name=row["meta.companyName"],
                rank=row['index'],
            )
            obj.save()

    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list('symbol', flat=True)
    base_url = ConfigSettings().get_conf("LIVE_INDEX_URL")
    url = ConfigSettings().get_conf("LIVE_INDEX_500_URL")
    obj = LiveStocks(
        base_url=base_url,
        url=url,
        symbols=symbols
    )
    df = obj.filter_stock_list()
    return update_five_hundred(data=df)


def analyse_stocks_five_hundred():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:
        if (
                (1 <= rec.rank <= 5) and
                (1 <= rec.last_price <= 4500) and
                (rec.percentage_change <= 11) and
                (rec.fhzero_set.all().count() <= 2) and
                (rec.fhzero_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]).count() == 0)
        ):
            five_hundred_zero = FhZero(
                date=datetime.now(),
                time=datetime.now().replace(tzinfo=get_current_timezone()),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY,
                quantity=int(20000/rec.last_price),
                last_price=rec.last_price
            )
            five_hundred_zero.save()

    return True

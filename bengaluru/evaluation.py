from datetime import datetime

from django.utils.timezone import get_current_timezone

from bengaluru.models import FhZero, FhZeroStatus, FiveHundred
from core.configuration import ConfigSettings
from core.stocks import LiveStocks


def update_five_hundred(data):
    FiveHundred.objects.filter(date=datetime.now()).update(rank=None)

    for index, row in data.iterrows():
        items = FiveHundred.objects.filter(date=datetime.now(), symbol=row["symbol"])
        if items:
            obj = items[0]
            obj.date = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                tzinfo=get_current_timezone()
            )
            obj.time = datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                tzinfo=get_current_timezone()
            )
            obj.rank = row["index"]
            obj.last_price = row["lastPrice"]
            obj.percentage_change = row["pChange"]
            obj.save()
        else:
            obj = FiveHundred(
                date=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                    tzinfo=get_current_timezone()
                ),
                time=datetime.strptime(row["lastUpdateTime"], "%d-%b-%Y %H:%M:%S").replace(
                    tzinfo=get_current_timezone()
                ),
                symbol=row["symbol"],
                identifier=row["identifier"],
                last_price=row["lastPrice"],
                percentage_change=row["pChange"],
                isin=row["meta.isin"],
                company_name=row["meta.companyName"],
                rank=row["index"],
            )
            obj.save()

    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list("symbol", flat=True)
    base_url = ConfigSettings().get_conf("LIVE_INDEX_URL")
    url = ConfigSettings().get_conf("LIVE_INDEX_500_URL")
    obj = LiveStocks(base_url=base_url, url=url, symbols=symbols)
    df = obj.filter_stock_list()
    return update_five_hundred(data=df)


def analyse_stocks_five_hundred():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:
        purchased_obj = rec.fhzero_set.filter(status=FhZeroStatus.PURCHASED)
        if 1 <= rec.rank <= 5 and rec.generate_fhz_evaluation:
            five_hundred_zero = FhZero(
                date=datetime.now(),
                time=datetime.now().replace(tzinfo=get_current_timezone()),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY,
                quantity=int(20000 / rec.last_price),
                last_price=rec.last_price,
            )
            five_hundred_zero.save()
        elif rec.rank > 5 and purchased_obj.count() == 1:
            fhz_obj = purchased_obj.first()
            fhz_obj.status = FhZeroStatus.TO_SELL
            fhz_obj.save()

    return True

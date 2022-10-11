from datetime import datetime

from django.utils.timezone import get_current_timezone
from django.conf import settings

from bengaluru.models import FhZero, FhZeroStatus, FiveHundred
from core.stocks import LiveStocks


LIVE_INDEX_URL = settings.LIVE_INDEX_URL
LIVE_INDEX_500_URL = settings.LIVE_INDEX_500_URL
FH_MAX_TOTAL_PRICE = settings.FH_MAX_TOTAL_PRICE  # 20000


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
    obj = LiveStocks(base_url=LIVE_INDEX_URL, url=LIVE_INDEX_500_URL, symbols=symbols)
    df = obj.filter_stock_list()
    return update_five_hundred(data=df)


def analyse_stocks_five_hundred():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:

        #  Buy condition check
        if rec.fhz_to_buy_condition:
            five_hundred_zero = FhZero(
                date=datetime.now(),
                time=datetime.now().replace(tzinfo=get_current_timezone()),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY,
                quantity=int(FH_MAX_TOTAL_PRICE / rec.last_price),
                last_price=rec.last_price,
            )
            five_hundred_zero.save()

        #  Sell condition check
        if rec.fhz_to_sell_condition:
            purchased_obj = rec.fhzero_set.filter(status=FhZeroStatus.PURCHASED)
            fhz_obj = purchased_obj.first()
            fhz_obj.status = FhZeroStatus.TO_SELL
            fhz_obj.save()

    return True


def process_five_hundred():
    fhz = FhZero.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.TO_SELL]
    ).order_by('updated_date').first()

    if not fhz:
        return None

    if fhz.status == FhZeroStatus.TO_BUY:
        fhz.status = FhZeroStatus.PURCHASED
        fhz.buy_price = fhz.five_hundred.last_price

    elif fhz.status == FhZeroStatus.TO_SELL:
        fhz.status = FhZeroStatus.SOLD
        fhz.sell_price = fhz.five_hundred.last_price
        fhz.profit_loss = fhz.buy_price - fhz.five_hundred.last_price

    fhz.save()

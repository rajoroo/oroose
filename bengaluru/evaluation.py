from datetime import datetime

from django.conf import settings

from bengaluru.models import FhZeroUpTrend, FhZeroDownTrend, FhZeroStatus, FiveHundred
from core.stocks import LiveStocks
# from core.zero_tool import fhz_buy_stock, fhz_maintain_stock, fhz_sell_stock
from core.zero_util import fhz_buy_stock, fhz_maintain_stock, fhz_sell_stock

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
            obj.rank = row["index"]
            obj.last_price = row["lastPrice"]
            obj.percentage_change = row["pChange"]
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
            )
            obj.save()

    return True


def polling_live_stocks_five_hundred():
    """Polling live stocks 500 and update the bengaluru with top 5 stocks"""
    symbols = FiveHundred.objects.filter(date=datetime.now()).values_list("symbol", flat=True)
    obj = LiveStocks(base_url=LIVE_INDEX_URL, url=LIVE_INDEX_500_URL, symbols=symbols)
    df = obj.filter_stock_list()
    return update_five_hundred(data=df)


def trigger_fhz_uptrend():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:

        #  Buy condition check
        if rec.fhz_uptrend_to_buy_condition():
            five_hundred_zero = FhZeroUpTrend(
                date=datetime.now(),
                time=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY,
                quantity=int(FH_MAX_TOTAL_PRICE / rec.last_price),
                # quantity=5,
                last_price=rec.last_price,
            )
            five_hundred_zero.save()

        #  Sell condition check
        if rec.fhz_uptrend_to_sell_condition():
            purchased_obj = rec.fhzerouptrend_set.filter(status=FhZeroStatus.PURCHASED)
            fhz_obj = purchased_obj.first()
            fhz_obj.status = FhZeroStatus.TO_SELL
            fhz_obj.save()

    return True


def trigger_fhz_downtrend():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:

        #  Sell condition check
        if rec.fhz_downtrend_to_sell_condition():
            five_hundred_zero = FhZeroDownTrend(
                date=datetime.now(),
                time=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_SELL,
                quantity=int(FH_MAX_TOTAL_PRICE / rec.last_price),
                # quantity=5,
                last_price=rec.last_price,
            )
            five_hundred_zero.save()

        #  Buy condition check
        if rec.fhz_downtrend_to_buy_condition():
            sold_obj = rec.fhzerodowntrend_set.filter(status=FhZeroStatus.SOLD)
            fhz_obj = sold_obj.first()
            fhz_obj.status = FhZeroStatus.TO_BUY
            fhz_obj.save()

    return True


def process_five_hundred():
    fhz = (
        FhZeroUpTrend.objects.filter(
            date=datetime.today(),
            error=False,
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.TO_SELL, FhZeroStatus.PURCHASED],
        )
    )

    if not fhz:
        return None

    for rec in fhz:
        if rec.status == FhZeroStatus.TO_BUY:
            print("TO BUY Started")
            fhz_buy_stock(fhz_obj=rec)

        elif rec.status == FhZeroStatus.PURCHASED:
            print("PURCHASED Started")
            fhz_maintain_stock(fhz_obj=rec)

        elif rec.status == FhZeroStatus.TO_SELL:
            print("TO SELL Started")
            fhz_sell_stock(fhz_obj=rec)

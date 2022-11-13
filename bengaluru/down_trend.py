from datetime import datetime, timedelta

from django.conf import settings

from bengaluru.models import FhZeroDownTrend, FhZeroStatus, FiveHundred
from core.zero_util import fhz_buy_stock, fhz_maintain_stock_downtrend, fhz_sell_stock

from core.models import ParameterSettings

LIVE_INDEX_URL = settings.LIVE_INDEX_URL
LIVE_INDEX_500_URL = settings.LIVE_INDEX_500_URL
FH_MAX_TOTAL_PRICE = settings.FH_MAX_TOTAL_PRICE  # 20000

FH_RANK_FROM = settings.FH_RANK_FROM  # 1
FH_RANK_TILL = settings.FH_RANK_TILL  # 5
FH_GRACE_RANK = settings.FH_GRACE_RANK  # 2
FH_MIN_PRICE = settings.FH_MIN_PRICE  # 20
FH_MAX_PRICE = settings.FH_MAX_PRICE  # 4500
FH_MAX_PERCENT = settings.FH_MAX_PERCENT  # 11
FH_MAX_BUY_ORDER = settings.FH_MAX_BUY_ORDER  # 2

FH_ZERO_START = settings.FH_ZERO_START
FH_ZERO_END = settings.FH_ZERO_END
SETTINGS_FH_ZERO = "SETTINGS_FH_ZERO"


def fhz_downtrend_to_sell_condition(fhz_obj):
    result = False

    ps = ParameterSettings.objects.get(name=SETTINGS_FH_ZERO)
    start = datetime.strptime(FH_ZERO_START, "%H%M").time()
    end = datetime.strptime(FH_ZERO_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)
    before_min = datetime.now() - timedelta(minutes=20)

    if (
            ps.status
            and (fhz_obj.rank > FH_RANK_TILL)
            and (FH_MIN_PRICE <= fhz_obj.last_price <= FH_MAX_PRICE)
            and (fhz_obj.percentage_change <= FH_MAX_PERCENT)
            and (fhz_obj.fhzerodowntrend_set.all().count() < FH_MAX_BUY_ORDER)
            and (not fhz_obj.fhzerodowntrend_set.filter(status__in=["TO_BUY", "SOLD", "TO_SELL"]).exists())
            and (start_time <= datetime.now() <= end_time)
            and (datetime.today().weekday() < 5)
    ):
        result = True

    if result and fhz_obj.fhzerodowntrend_set.all():
        latest_fhz = fhz_obj.fhzerodowntrend_set.latest("updated_date")
        if latest_fhz.updated_date > before_min:
            result = False

    return result


def fhz_downtrend_to_buy_condition(fhz_obj):
    result = False
    ps = ParameterSettings.objects.get(name=SETTINGS_FH_ZERO)
    if (
            ps.status
            and fhz_obj.rank < FH_RANK_TILL
            and fhz_obj.fhzerodowntrend_set.filter(status=FhZeroStatus.SOLD).exists()
    ):
        result = True

    return result


def trigger_fhz_downtrend():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:

        #  Sell condition check
        if fhz_downtrend_to_sell_condition(fhz_obj=rec):
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
        if fhz_downtrend_to_buy_condition(fhz_obj=rec):
            sold_obj = rec.fhzerodowntrend_set.filter(status=FhZeroStatus.SOLD)
            fhz_obj = sold_obj.first()
            fhz_obj.status = FhZeroStatus.TO_BUY
            fhz_obj.save()

    return True


def process_fhz_downtrend():
    fhz = (
        FhZeroDownTrend.objects.filter(
            date=datetime.today(),
            error=False,
            status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.TO_SELL, FhZeroStatus.SOLD],
        )
    )

    if not fhz:
        return None

    for rec in fhz:
        if rec.status == FhZeroStatus.TO_BUY:
            print("TO BUY Started")
            fhz_buy_stock(fhz_obj=rec)

        elif rec.status == FhZeroStatus.SOLD:
            print("PURCHASED Started")
            fhz_maintain_stock_downtrend(fhz_obj=rec)

        elif rec.status == FhZeroStatus.TO_SELL:
            print("TO SELL Started")
            fhz_sell_stock(fhz_obj=rec)

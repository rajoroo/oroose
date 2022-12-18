from datetime import datetime, timedelta

from bengaluru.models import FhZeroUpTrend, FhZeroStatus, FiveHundred
from core.zero_util import fhz_buy_stock, fhz_maintain_stock_uptrend, fhz_sell_stock
from core.models import ParameterSettings
from core.constant import SETTINGS_FHZ_UPTREND
from bengaluru.constant import (
    FH_RANK_FROM,
    FH_RANK_TILL,
    FH_GRACE_RANK,
    FH_MIN_PRICE,
    FH_MAX_PRICE,
    FH_MAX_TOTAL_PRICE,
    FH_MAX_PERCENT,
    FH_MAX_BUY_ORDER,
    BENGALURU_START,
    BENGALURU_END,
)


def fhz_uptrend_to_buy_condition(fhz_obj):
    result = False

    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_UPTREND)
    start = datetime.strptime(BENGALURU_START, "%H%M").time()
    end = datetime.strptime(BENGALURU_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)
    before_min = datetime.now() - timedelta(minutes=20)

    if (
        ps.status
        and (FH_RANK_FROM <= fhz_obj.rank <= FH_RANK_TILL - 1)
        and (FH_MIN_PRICE <= fhz_obj.last_price <= FH_MAX_PRICE)
        and (fhz_obj.percentage_change <= FH_MAX_PERCENT)
        and (fhz_obj.fhzerouptrend_set.all().count() < FH_MAX_BUY_ORDER)
        and (not fhz_obj.fhzerouptrend_set.filter(status__in=["TO_BUY", "PURCHASED", "TO_SELL"]).exists())
        and (start_time <= datetime.now() <= end_time)
        and (datetime.today().weekday() < 5)
        and (fhz_obj.previous_rank > fhz_obj.rank)
    ):
        result = True

    if result and fhz_obj.fhzerouptrend_set.all():
        latest_fhz = fhz_obj.fhzerouptrend_set.latest("updated_date")
        if latest_fhz.updated_date > before_min:
            result = False

    return result


def fhz_uptrend_to_sell_condition(fhz_obj):
    result = False
    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_UPTREND)
    if (
        ps.status
        and fhz_obj.rank > FH_RANK_TILL + FH_GRACE_RANK
        and fhz_obj.fhzerouptrend_set.filter(status=FhZeroStatus.PURCHASED).exists()
    ):
        result = True

    return result


def trigger_fhz_uptrend():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:

        #  Buy condition check
        if fhz_uptrend_to_buy_condition(fhz_obj=rec):
            five_hundred_zero = FhZeroUpTrend(
                date=datetime.now(),
                time=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY,
                quantity=int(FH_MAX_TOTAL_PRICE / rec.last_price),
                # quantity=1,
                last_price=rec.last_price,
            )
            five_hundred_zero.save()

        #  Sell condition check
        if fhz_uptrend_to_sell_condition(fhz_obj=rec):
            purchased_obj = rec.fhzerouptrend_set.filter(status=FhZeroStatus.PURCHASED)
            fhz_obj = purchased_obj.first()
            fhz_obj.status = FhZeroStatus.TO_SELL
            fhz_obj.save()

    return True


def process_fhz_uptrend():
    fhz = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        error=False,
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.TO_SELL, FhZeroStatus.PURCHASED],
    )

    if not fhz:
        return None

    for rec in fhz:
        if rec.status == FhZeroStatus.TO_BUY:
            print("TO BUY Started")
            fhz_buy_stock(fhz_obj=rec)

        elif rec.status == FhZeroStatus.PURCHASED:
            print("PURCHASED Started")
            fhz_maintain_stock_uptrend(fhz_obj=rec)

        elif rec.status == FhZeroStatus.TO_SELL:
            print("TO SELL Started")
            fhz_sell_stock(fhz_obj=rec)

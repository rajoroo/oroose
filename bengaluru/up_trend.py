from datetime import datetime, timedelta

from bengaluru.constant import (  # FH_GRACE_RANK,
    BENGALURU_END,
    BENGALURU_START,
    FH_MAX_BUY_ORDER,
    FH_MAX_PERCENT,
    FH_MAX_PRICE,
    FH_MAX_TOTAL_PRICE,
    FH_MIN_PRICE,
    FH_RANK_FROM,
    FH_RANK_TILL,
)
from bengaluru.models import FhZeroUpTrend
from core.choice import FhZeroStatus, PlStatus
from core.constant import SETTINGS_FHZ_UPTREND
from core.models import ParameterSettings
from core.zero_util import fhz_buy_stock, fhz_maintain_stock_uptrend, fhz_sell_stock
from stockwatch.choice import SignalStatus
from stockwatch.models import FiveHundred


def fhz_uptrend_to_buy_condition(fhz_obj):
    result = False
    basic_requirement = False
    pre_order_requirement = True
    standard_requirement = False

    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_UPTREND)
    start = datetime.strptime(BENGALURU_START, "%H%M").time()
    end = datetime.strptime(BENGALURU_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)
    before_20_min = datetime.now() - timedelta(minutes=20)
    fhz_status = [FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL]
    pl_status = [PlStatus.WINNER, PlStatus.INPROG]

    if (
        ps.status
        and fhz_obj.is_valid is True
        # and (fhz_obj.pp > fhz_obj.pp1 > 65 > fhz_obj.pp2)
        and (fhz_obj.rank <= 9)
        and (FH_MIN_PRICE <= fhz_obj.last_price <= FH_MAX_PRICE)
        and (fhz_obj.percentage_change <= FH_MAX_PERCENT)
        and (fhz_obj.fhzerouptrend_set.all().count() < FH_MAX_BUY_ORDER)
        and (not fhz_obj.fhzerouptrend_set.filter(status__in=fhz_status).exists())
        and (not fhz_obj.fhzerouptrend_set.filter(pl_status__in=pl_status).exists())
        and (not fhz_obj.fhzerouptrend_set.filter(error=True).exists())
        and (start_time <= datetime.now() <= end_time)
        and (datetime.today().weekday() < 5)
    ):
        basic_requirement = True

    if fhz_obj.fhzerouptrend_set.all():
        latest_fhz = fhz_obj.fhzerouptrend_set.latest("updated_date")
        if latest_fhz.updated_date > before_20_min:
            pre_order_requirement = False

    if (
        fhz_obj.pp
        and fhz_obj.pp1
        and fhz_obj.pp2
        and fhz_obj.pp_price
        and fhz_obj.pp1_price
        and fhz_obj.pp2_price
        and (
            (fhz_obj.pp > fhz_obj.pp1 > 65 > fhz_obj.pp2)
            or (
                (fhz_obj.rank <= 5)
                and (fhz_obj.pp_price > fhz_obj.pp1_price > fhz_obj.pp2_price)
                and (60 < fhz_obj.pp < 80)
            )
        )
    ):
        standard_requirement = True

    if basic_requirement and pre_order_requirement and standard_requirement:
        result = True
    print(basic_requirement, pre_order_requirement, standard_requirement)
    return result


def fhz_uptrend_maintain_order(fhz_obj):
    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_UPTREND)
    purchased_obj = fhz_obj.fhzerouptrend_set.filter(status=FhZeroStatus.PURCHASED).first()
    if (
        ps.status
        # and fhz_obj.pp
        # and fhz_obj.pp1
        # and fhz_obj.pp2
        # and ((fhz_obj.pp1 < 65) or (fhz_obj.pp < 65))
        # and (pre_signal_status == signal_status == SignalStatus.SELL)
        # and fhz_obj.fhzerouptrend_set.filter(status=FhZeroStatus.PURCHASED).exists()
        and purchased_obj
    ):
        purchased_obj.maintain_order()

    return True


def trigger_fhz_uptrend():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:

        # Maintain Order
        purchased_obj = rec.fhzerouptrend_set.filter(status=FhZeroStatus.PURCHASED).first()
        if purchased_obj:
            purchased_obj.maintain_order()
            # return True

        #  Buy condition check
        if fhz_uptrend_to_buy_condition(fhz_obj=rec):
            five_hundred_zero = FhZeroUpTrend(
                date=datetime.now(),
                created_date=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY,
                quantity=int(FH_MAX_TOTAL_PRICE / rec.last_price),
                # quantity=1,
                last_price=rec.last_price,
                pl_status=PlStatus.INPROG,
                rank=rec.rank,
            )
            five_hundred_zero.save()

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
            rec.buy_order()

        # elif rec.status == FhZeroStatus.PURCHASED:
        #     rec.maintain_order()

        elif rec.status == FhZeroStatus.TO_SELL:
            rec.sell_order()


def uptrend_panic_pull():
    fhz = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL],
        error=False,
    )
    if not fhz:
        return None

    for rec in fhz:
        rec.sell_order()

    return True

from datetime import datetime, timedelta

from core.choice import FhZeroStatus, PlStatus
from core.constant import SETTINGS_FHZ_DOWNTREND
from core.models import ParameterSettings
from core.zero_util import fhz_buy_stock, fhz_maintain_stock_downtrend, fhz_sell_stock
from mysuru.constant import (
    FH_MAX_BUY_ORDER,
    FH_MAX_PERCENT,
    FH_MAX_PRICE,
    FH_MAX_TOTAL_PRICE,
    FH_MIN_PRICE,
    MYSURU_END,
    MYSURU_START,
)
from mysuru.models import FhZeroDownTrend
from stockwatch.choice import SignalStatus
from stockwatch.models import FiveHundred


def fhz_downtrend_to_sell_condition(fhz_obj):
    result = False

    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_DOWNTREND)
    start = datetime.strptime(MYSURU_START, "%H%M").time()
    end = datetime.strptime(MYSURU_END, "%H%M").time()
    start_time = datetime.combine(datetime.today(), start)
    end_time = datetime.combine(datetime.today(), end)
    before_20_min = datetime.now() - timedelta(minutes=20)
    fhz_status = [FhZeroStatus.TO_BUY, FhZeroStatus.SOLD, FhZeroStatus.TO_SELL]
    pl_status = [PlStatus.WINNER, PlStatus.INPROG]

    if (
        ps.status
        and fhz_obj.is_valid is True
        and (fhz_obj.pp1 < 70 < fhz_obj.pp2)
        and (fhz_obj.pp < 70 < fhz_obj.pp2)
        # and (fhz_obj.signal_status == SignalStatus.SELL)
        and (fhz_obj.rank <= 9)
        and (FH_MIN_PRICE <= fhz_obj.last_price <= FH_MAX_PRICE)
        and (fhz_obj.percentage_change <= FH_MAX_PERCENT)
        and (fhz_obj.fhzerodowntrend_set.all().count() <= FH_MAX_BUY_ORDER)
        and (not fhz_obj.fhzerodowntrend_set.filter(status__in=fhz_status).exists())
        and (not fhz_obj.fhzerodowntrend_set.filter(pl_status__in=pl_status).exists())
        and (not fhz_obj.fhzerodowntrend_set.filter(error=True).exists())
        and (start_time <= datetime.now() <= end_time)
        and (datetime.today().weekday() < 5)
    ):
        result = True

    # if result and fhz_obj.fhzerodowntrend_set.all():
    #     latest_fhz = fhz_obj.fhzerodowntrend_set.latest("updated_date")
    #     if latest_fhz.updated_date > before_20_min:
    #         result = False

    return result


def fhz_downtrend_to_buy_condition(fhz_obj):
    result = False
    ps = ParameterSettings.objects.get(name=SETTINGS_FHZ_DOWNTREND)

    if (
        ps.status
        and (fhz_obj.pp1 > 70 > fhz_obj.pp2)
        and (fhz_obj.pp > 70 > fhz_obj.pp2)
        # and (fhz_obj.signal_status == SignalStatus.BUY)
        and fhz_obj.fhzerodowntrend_set.filter(status=FhZeroStatus.SOLD).exists()
    ):
        result = True

    sold_obj = fhz_obj.fhzerodowntrend_set.filter(status=FhZeroStatus.SOLD, error=False)

    if sold_obj:
        sold_fhz = sold_obj.first()
        price = sold_fhz.sell_price
        lower_circuit = price + (price * 0.003)

        if sold_fhz.current_price >= lower_circuit:
            result = True

    return result


def trigger_fhz_downtrend():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    for rec in five_hundred:

        #  Sell condition check
        if fhz_downtrend_to_sell_condition(fhz_obj=rec):
            five_hundred_zero = FhZeroDownTrend(
                date=datetime.now(),
                created_date=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_SELL,
                quantity=int(FH_MAX_TOTAL_PRICE / rec.last_price),
                # quantity=1,
                last_price=rec.last_price,
                pl_status=PlStatus.INPROG,
                rank=rec.rank,
            )
            five_hundred_zero.save()

        #  Buy condition check
        if fhz_downtrend_to_buy_condition(fhz_obj=rec):
            sold_obj = rec.fhzerodowntrend_set.filter(status=FhZeroStatus.SOLD, error=False)
            fhz_obj = sold_obj.first()
            fhz_obj.status = FhZeroStatus.TO_BUY
            fhz_obj.save()

    return True


def process_fhz_downtrend():
    fhz = FhZeroDownTrend.objects.filter(
        date=datetime.today(),
        error=False,
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.TO_SELL, FhZeroStatus.SOLD],
    )

    if not fhz:
        return None

    for rec in fhz:
        if rec.status == FhZeroStatus.TO_SELL:
            fhz_sell_stock(fhz_obj=rec)

        elif rec.status == FhZeroStatus.SOLD:
            fhz_maintain_stock_downtrend(fhz_obj=rec)

        elif rec.status == FhZeroStatus.TO_BUY:
            fhz_buy_stock(fhz_obj=rec)
            rec.pl_status = PlStatus.RUNNER
            rec.save()


def downtrend_panic_pull():
    fhz = FhZeroDownTrend.objects.filter(
        date=datetime.today(),
        status__in=[FhZeroStatus.SOLD, FhZeroStatus.TO_BUY],
        error=False,
    )
    if not fhz:
        return None

    for rec in fhz:
        fhz_buy_stock(fhz_obj=rec)

    return True

from datetime import datetime, timedelta

from bengaluru.models import FhZeroUpTrend
from core.choice import FhZeroStatus, PlStatus
from stockwatch.models import FiveHundred
from core.tools import get_param_config_tag, get_today_datetime


# def fhz_uptrend_to_buy_condition(fhz_obj):
#     basic_requirement = False
#     pre_order_requirement = True
#     standard_requirement = False
#
#     config = get_param_config_tag(tag="BENGALURU")
#     start_time = get_today_datetime(time_str=config.get("start_time"))
#     end_time = get_today_datetime(time_str=config.get("end_time"))
#     before_20_min = datetime.now() - timedelta(minutes=20)
#     fhz_status = [FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL]
#     pl_status = [PlStatus.WINNER, PlStatus.INPROG]
#
#     if (
#         config.get("bengaluru_status")
#         and fhz_obj.is_valid is True
#         and (fhz_obj.rank <= 9)
#         and (config["min_price"] <= fhz_obj.last_price <= config["max_price"])
#         and (fhz_obj.percentage_change <= config["max_percentage"])
#         and (fhz_obj.fhzerouptrend_set.all().count() < config["max_buy_order"])
#         and (not fhz_obj.fhzerouptrend_set.filter(status__in=fhz_status).exists())
#         and (not fhz_obj.fhzerouptrend_set.filter(pl_status__in=pl_status).exists())
#         and (not fhz_obj.fhzerouptrend_set.filter(error=True).exists())
#         and (start_time <= datetime.now() <= end_time)
#         and (datetime.today().weekday() < 5)
#         and fhz_obj.pp
#         and fhz_obj.pp1
#         and fhz_obj.pp2
#         and fhz_obj.pp_price
#         and fhz_obj.pp1_price
#         and fhz_obj.pp2_price
#     ):
#         basic_requirement = True
#
#     if fhz_obj.fhzerouptrend_set.all():
#         latest_fhz = fhz_obj.fhzerouptrend_set.latest("updated_date")
#         if latest_fhz.updated_date > before_20_min:
#             pre_order_requirement = False
#
#     # Return False is the condition didn't pass basic and pre-order requirement
#     if not (basic_requirement and pre_order_requirement):
#         return False
#
#     if (
#         (fhz_obj.pp > fhz_obj.pp1 > 65 > fhz_obj.pp2)
#         or (
#             (fhz_obj.rank <= 5)
#             and (fhz_obj.pp_price > fhz_obj.pp1_price > fhz_obj.pp2_price)
#             and (60 < fhz_obj.pp < 80)
#         )
#     ):
#         standard_requirement = True
#
#     return standard_requirement


def generate_bengaluru():
    five_hundred = FiveHundred.objects.filter(date=datetime.today())
    config = get_param_config_tag(tag="BENGALURU")
    for rec in five_hundred:
        #  Buy condition check
        if rec.get_standard_requirement():
            five_hundred_zero = FhZeroUpTrend(
                date=datetime.now(),
                created_date=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=FhZeroStatus.TO_BUY,
                quantity=int(config["max_total_price"] / rec.last_price),
                # quantity=1,
                last_price=rec.last_price,
                pl_status=PlStatus.INPROG,
                rank=rec.rank,
            )
            five_hundred_zero.save()

    return True


def maintain_bengaluru():
    """Maintain order happens with every 5 min"""
    recs = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        error=False,
        status=FhZeroStatus.PURCHASED,
    )
    for rec in recs:
        purchased_obj = rec.fhzerouptrend_set.filter(status=FhZeroStatus.PURCHASED).first()
        if purchased_obj:
            purchased_obj.maintain_order()


def process_fhz_uptrend():
    fhz = FhZeroUpTrend.objects.filter(
        date=datetime.today(),
        error=False,
        status__in=[FhZeroStatus.TO_BUY, FhZeroStatus.TO_SELL],
    )

    if not fhz:
        return None

    for rec in fhz:
        if rec.status == FhZeroStatus.TO_BUY:
            rec.buy_order()

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

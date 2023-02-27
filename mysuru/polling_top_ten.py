from datetime import datetime
from django.db.models import F
from mysuru.models import TopTen, MysuruTrend, PlStatus, TrendStatus,DayStatus
from stockwatch.models import StockWatchFh
import random
from core.tools import get_param_config_tag


def polling_top_ten_stocks():
    obj = StockWatchFh.objects.all().order_by("-id").first()
    if (not obj) and (not hasattr(obj, "stock_data")):
        return False

    TopTen.objects.all().delete()
    for key, value in obj.stock_data.items():
        tt = TopTen.objects.create(
            date=datetime.today(),
            symbol=value["symbol"],
            identifier=value["identifier"],
            isin=value["isin"],
            company_name=value["company_name"],
            last_price=value["last_price"],
            percentage_change=value["percentage_change"],
        )
        tt.get_smart_token()
        tt.is_valid_stock()
    return True


def process_top_ten_get_year_macd():
    recs = TopTen.objects.filter(is_valid=True, ema_200__isnull=True)[:50]
    for rec in recs:
        rec.get_year_macd()
        rec.get_day_macd()
        rec.get_day_status()


def process_top_ten_accepted():
    accepted = TopTen.objects.filter(is_accepted=True).exists()
    if accepted:
        return True

    recs = TopTen.objects.filter(day_status=DayStatus.YES).values_list('pk', flat=True)
    vals = random.sample(list(recs), 5)
    for val in vals:
        obj = TopTen.objects.get(pk=val)
        obj.is_accepted = True
        obj.save()


def trigger_accepted_top_ten():
    top_ten_exists = TopTen.objects.filter(is_valid=True, ema_200__isnull=True).exists()
    if top_ten_exists:
        process_top_ten_get_year_macd()
    else:
        process_top_ten_accepted()

    return True


def process_top_ten_get_macd():
    recs = TopTen.objects.filter(is_accepted=True)
    for rec in recs:
        rec.get_macd()


def generate_mysuru():
    top_ten = TopTen.objects.filter(is_accepted=True)
    config = get_param_config_tag(tag="MYSURU")
    for rec in top_ten:
        #  Buy condition check
        if rec.get_standard_requirement():
            mysuru = MysuruTrend(
                date=datetime.now(),
                created_date=datetime.now(),
                symbol=rec.symbol,
                isin=rec.isin,
                five_hundred=rec,
                status=TrendStatus.TO_BUY,
                # quantity=int(config["max_total_price"] / rec.last_price),
                quantity=1,
                last_price=rec.last_price,
                pl_status=PlStatus.INPROG,
                rank=rec.rank,
            )
            mysuru.save()

    return True


def maintain_mysuru():
    """Maintain order happens with every 5 min"""
    recs = MysuruTrend.objects.filter(
        date=datetime.today(),
        error=False,
        status=TrendStatus.PURCHASED,
    )
    for rec in recs:
        purchased_obj = rec.mysurutrend_set.filter(status=TrendStatus.PURCHASED).first()
        if purchased_obj:
            purchased_obj.maintain_order()


def process_mysuru_trend():
    mysuru = MysuruTrend.objects.filter(
        date=datetime.today(),
        error=False,
        status__in=[TrendStatus.TO_BUY, TrendStatus.TO_SELL],
    )

    if not mysuru:
        return None

    for rec in mysuru:
        if rec.status == TrendStatus.TO_BUY:
            rec.buy_order()

        elif rec.status == TrendStatus.TO_SELL:
            rec.sell_order()


def mysuru_trend_panic_pull():
    mysuru = MysuruTrend.objects.filter(
        date=datetime.today(),
        status__in=[TrendStatus.PURCHASED, TrendStatus.TO_SELL],
        error=False,
    )
    if not mysuru:
        return None

    for rec in mysuru:
        rec.sell_order()

    return True

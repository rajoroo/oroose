from datetime import datetime
from mysuru.models import TopTen, DayStatus
from stockwatch.models import StockWatchFh
import random


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


def trigger_calculate_top_ten():
    recs = TopTen.objects.filter(is_valid=True, ema_200__isnull=True)[:100]
    for rec in recs:
        rec.generate_macd_osc()
        rec.get_day_status()
    return True


def trigger_validate_top_ten():
    is_crawl_not_completed = TopTen.objects.filter(is_valid=True, ema_200__isnull=True).exists()
    if is_crawl_not_completed:
        return True

    recs = TopTen.objects.filter(day_status=DayStatus.YES).values_list('pk', flat=True)
    vals = random.sample(list(recs), 5)
    for val in vals:
        obj = TopTen.objects.get(pk=val)
        obj.is_accepted = True
        obj.save()
    return True

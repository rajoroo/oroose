from datetime import datetime
from mysuru.models import TopTen, DayStatus
from .stocks import LiveStocks
from django.conf import settings
import random


def polling_top_ten_stocks():
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL)

    # Get live data, feed data, save data
    obj.get_live_data()
    obj.save_stock_data()
    # obj.get_feed_data()

    # Raw data
    stock_data = obj.get_live_stock_list()
    TopTen.objects.all().delete()

    for index, row in stock_data.iterrows():
        tt = TopTen.objects.create(
            date=datetime.today(),
            symbol=row["symbol"],
            identifier=row["identifier"],
            isin=row["meta.isin"],
            company_name=row["meta.companyName"],
            last_price=row["lastPrice"],
            percentage_change=row["pChange"],
        )
        tt.get_smart_token()
    return True


def trigger_calculate_top_ten():
    recs = TopTen.objects.filter(ema_200__isnull=True)[:100]
    for rec in recs:
        rec.generate_macd_osc()
        rec.get_day_status()
    return True


def trigger_validate_top_ten():
    is_crawl_not_completed = TopTen.objects.filter(ema_200__isnull=True).exists()
    if is_crawl_not_completed:
        return True

    recs = TopTen.objects.filter(day_status=DayStatus.YES).values_list('pk', flat=True)
    vals = random.sample(list(recs), 5)
    for val in vals:
        obj = TopTen.objects.get(pk=val)
        obj.is_accepted = True
        obj.save()
    return True

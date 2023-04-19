from datetime import datetime
from mysuru.models import MacdTrend
from .stocks import LiveStocks
from django.conf import settings
from django.db.models import Q


def polling_macd_stocks():
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL)

    # Get live data, feed data, save data
    obj.get_live_data()
    obj.save_stock_data()
    # obj.get_feed_data()

    # Raw data
    stock_data = obj.get_live_stock_list()
    MacdTrend.objects.all().delete()

    for index, row in stock_data.iterrows():
        tt = MacdTrend.objects.create(
            date=datetime.today(),
            symbol=row["symbol"],
            identifier=row["identifier"],
            isin=row["meta.isin"],
            company_name=row["meta.companyName"],
            price=row["lastPrice"],
            percentage_change=row["pChange"],
        )
        tt.get_smart_token()
    return True


def check_update_latest_date():
    latest_date = MacdTrend.objects.filter(ema_200__isnull=False).latest('updated_date').updated_date
    if latest_date:
        recs = MacdTrend.objects.filter(~Q(updated_date=latest_date), ema_200__isnull=False)
        for rec in recs:
            rec.ema_200 = None
            rec.save()


def calculate_macd():
    recs = MacdTrend.objects.filter(ema_200__isnull=True)[:500]
    for rec in recs:
        rec.generate_macd_osc()
        rec.get_day_status()


def trigger_calculate_macd():
    calculate_macd()
    check_update_latest_date()
    return True

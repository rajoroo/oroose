from datetime import datetime

from django.conf import settings
from django.db.models import Q

from mysuru.models import StochDailyTrend

from .stocks import LiveStocks
import io
import pandas as pd


def polling_stoch_stocks():
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL)

    # Get live data, feed data, save data
    obj.get_live_data()
    obj.save_stock_data()
    # obj.get_feed_data()

    # Raw data
    stock_data = obj.get_live_stock_list()
    StochDailyTrend.objects.all().delete()

    for index, row in stock_data.iterrows():
        tt = StochDailyTrend.objects.create(
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
    latest_date = StochDailyTrend.objects.filter(ema_200__isnull=False).latest("updated_date").updated_date
    if latest_date:
        recs = StochDailyTrend.objects.filter(~Q(updated_date=latest_date), ema_200__isnull=False)
        for rec in recs:
            rec.ema_200 = None
            rec.save()


def calculate_stoch():
    recs = StochDailyTrend.objects.filter(ema_200__isnull=True)[:500]
    for rec in recs:
        rec.generate_stoch()
        rec.get_day_status()


def trigger_calculate_stoch():
    calculate_stoch()
    check_update_latest_date()
    return True


def polling_bhav_copy():
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.BHAV_URL)
    stock_data = obj.get_bhav_data()

    StochDailyTrend.objects.all().delete()

    for index, row in stock_data.iterrows():
        tt = StochDailyTrend.objects.create(
            date=datetime.today(),
            symbol=row["SYMBOL"],
            identifier=row["SYMBOL"],
            isin=row["ISIN"],
            company_name=row["SYMBOL"],
            price=row["LAST"],
            percentage_change=row["LAST"],
        )
        tt.get_smart_token()
    return True


def handle_upload_stoch_stocks(csv_file):
    # Raw data
    csv_data = io.StringIO(csv_file.read().decode("utf-8"))
    stock_data = pd.read_csv(csv_data)
    StochDailyTrend.objects.all().delete()

    for index, row in stock_data.iterrows():
        tt = StochDailyTrend.objects.create(date=datetime.today(), symbol=row["SYMBOL"])
        tt.get_smart_token()
    return True

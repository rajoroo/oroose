from datetime import datetime

from django.conf import settings
from django.db.models import Q

from mysuru.models import StochDailyTrend

from .stocks import LiveStocks
import io
import pandas as pd


def fetch_stocks(model_obj):
    """Fetch stocks from Live stocks"""
    obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL)

    # Get live data, feed data, save data
    obj.get_live_data()
    obj.save_stock_data()

    # Raw data
    stock_data = obj.get_live_stock_list()
    model_obj.objects.all().delete()

    create_list = []
    for index, row in stock_data.iterrows():
        create_list.append(
            model_obj(
                symbol=row["symbol"],
                company_name=row["meta.companyName"],
            )
        )
    model_obj.objects.bulk_create(create_list)
    recs = model_obj.objects.all()
    for rec in recs:
        rec.get_smart_token()

    model_obj.objects.filter(smart_token__isnull=True, smart_token_fetched=True).delete()
    return True


def fetch_trend_value(model_obj):
    """Fetch trend value"""
    recs = model_obj.objects.filter(is_fetched=False)[:500]
    for rec in recs:
        rec.generate_trend_value()

    return True


def reset_fetched(model_obj):
    """Reset fetch flag"""
    if not model_obj.objects.filter(is_fetched=False):
        model_obj.objects.all().update(is_fetched=False)

    return True
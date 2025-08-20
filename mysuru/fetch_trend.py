from datetime import datetime

from django.conf import settings
from django.db.models import F, Q

from core.telegram_util import TelegramAlert
from .stocks import LiveStocks
import io
import pandas as pd
from mysuru.models import StockData
from core.smart_util import download_future


class FetchTrend:
    def __init__(self):
        """Initialization of fetch trend"""
        self.model_obj = StockData
        self.stock_data = None

    def fetch_trend_value(self, data_type):
        """Fetch trend value"""
        filter_params = {f"is_{data_type}_fetched": False}
        recs = self.model_obj.objects.filter(**filter_params)[:500]
        for rec in recs:
            rec.generate_trend_value(data_type=data_type)

        return True

    def trend_reset(self, data_type):
        """Fetch potential trend value"""
        filter_params = {f"is_{data_type}_fetched": True}
        update_params = {f"is_{data_type}_fetched": False}
        recs = self.model_obj.objects.filter(**filter_params)
        recs.update(**update_params)
        return True


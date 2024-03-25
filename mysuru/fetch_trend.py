from datetime import datetime

from django.conf import settings

from .stocks import LiveStocks
import io
import pandas as pd
from mysuru.models import HourlyTrend, DailyTrend, WeeklyTrend


class FetchTrend:
    def __init__(self, model_obj):
        """Initialization of fetch trend"""
        self.model_obj = model_obj
        self.stock_data = None

    def fetch_live_stocks(self):
        """Fetch stocks from Live stocks"""
        obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_INDEX_500_URL)

        # Get live data, feed data, save data
        obj.get_live_data()
        obj.save_stock_data()

        # Raw data
        stock_data = obj.get_live_stock_list()

        self.stock_data = [
            {"symbol": row["Symbol"], "company_name": row["Company Name"]} for index, row in stock_data.iterrows()
        ]
        return True

    def fetch_bhav_copy(self):
        """Fetch bhav copy"""
        obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.BHAV_URL)
        stock_data = obj.get_bhav_data()

        self.stock_data = [
            {"symbol": row["SYMBOL"], "company_name": row["SYMBOL"]} for index, row in stock_data.iterrows()
        ]
        return True

    def fetch_futures_stocks(self):
        obj = LiveStocks(base_url=settings.LIVE_INDEX_URL, url=settings.LIVE_FUTURES_URL)

        # Get live data, feed data, save data
        obj.get_live_data()
        obj.save_stock_data()

        # Raw data
        stock_data = obj.get_futures_stock_list()
        self.stock_data = [
            {"symbol": row["symbol"], "company_name": row["underlying"]} for index, row in stock_data.iterrows()
        ]
        return True

    def handle_upload_stoch_stocks(self, csv_file):
        """Process data from uploaded CSV file"""
        # Raw data
        csv_data = io.StringIO(csv_file.read().decode("utf-8"))
        stock_data = pd.read_csv(csv_data)

        self.stock_data = [
            {"symbol": row["SYMBOL"], "company_name": row["SYMBOL"]} for index, row in stock_data.iterrows()
        ]
        return True

    def create_trend(self):
        """Generate stock in trend model"""
        self.model_obj.objects.all().delete()

        create_list = []
        for row in self.stock_data:
            create_list.append(
                self.model_obj(
                    symbol=row["symbol"],
                    company_name=row["company_name"],
                )
            )
        self.model_obj.objects.bulk_create(create_list)
        recs = self.model_obj.objects.all()
        for rec in recs:
            rec.get_smart_token()

        self.model_obj.objects.filter(smart_token__isnull=True, smart_token_fetched=True).delete()
        return True

    def fetch_trend_value(self):
        """Fetch trend value"""
        recs = self.model_obj.objects.filter(is_fetched=False)[:500]
        for rec in recs:
            rec.generate_trend_value()

        return True

    def reset_fetched(self):
        """Reset fetch flag"""
        if not self.model_obj.objects.filter(is_fetched=False):
            self.model_obj.objects.all().update(is_fetched=False)

        return True


def get_model_object(name):
    """Get model object from name"""
    model_obj = None
    if name == "hourly":
        model_obj = HourlyTrend
    elif name == "daily":
        model_obj = DailyTrend
    elif name == "weekly":
        model_obj = WeeklyTrend

    return model_obj

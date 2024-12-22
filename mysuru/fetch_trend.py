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

    def fetch_futures_stocks_smart(self):
        stock_data = download_future()
        self.stock_data = [
            {"symbol": row["name"], "company_name": row["name"]} for index, row in stock_data.iterrows()
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

    def fetch_trend_m15_short_value(self, data_type):
        """Fetch trend value"""
        filter_params = {
            "is_wk_fetched": True,
            "is_day_fetched": True,
            "is_m15_fetched": False,
            "wk_rsi_0__gt": 60,
            "day_rsi_0__gt": 60,
        }
        recs = self.model_obj.objects.filter(**filter_params)
        for rec in recs:
            rec.generate_trend_value(data_type=data_type)

        return True

    def fetch_trend_value(self, data_type):
        """Fetch trend value"""
        filter_params = {f"is_{data_type}_fetched": False}
        recs = self.model_obj.objects.filter(**filter_params)[:500]
        for rec in recs:
            rec.generate_trend_value(data_type=data_type)

        return True

    def fetch_potential_trend_value(self, data_type):
        """Fetch potential trend value"""
        filter_params = {
            "is_wk_fetched": True,
            "wk_ema_200_1__lt": F("wk_ema_20_1"),
            "wk_ema_50_1__lt": F("wk_ema_20_1"),
            "wk_ha_open_1__lt": F("wk_ha_close_1"),
            "wk_ema_20_1__lt": F("wk_ha_open_1"),
            "wk_rsi_1__gt": 60,
            f"is_{data_type}_fetched": False,
        }
        recs = self.model_obj.objects.filter(**filter_params)[:500]
        for rec in recs:
            rec.generate_trend_value(data_type=data_type)

        return True

    def fetch_trading_value(self, data_type):
        """Fetch potential trend value"""
        filter_params = {
            "is_trading": True,
        }
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

    def raise_alert_message(self):
        # Up Values
        recs = self.model_obj.objects.filter(is_trading=True, trading_status="up")
        for rec in recs:
            print(f"EMA: {rec.m5_ema_20_0} Close: {rec.m5_ha_close_0}")
        recs = recs.filter(Q(m5_ema_20_0__gt=F("m5_ha_close_0")) & Q(m5_ema_20_0__gt=F("m5_ha_open_0"))).values_list(
            "symbol", flat=True
        )
        if recs:
            symbols = "\n".join(recs)
            TelegramAlert.send_message(symbols)

        # Down Values
        recs = self.model_obj.objects.filter(is_trading=True, trading_status="dn")
        for rec in recs:
            print(f"EMA: {rec.m5_ema_20_0} Close: {rec.m5_ha_close_0}")
        recs = recs.filter(Q(m5_ema_20_0__lt=F("m5_ha_close_0")) & Q(m5_ema_20_0__lt=F("m5_ha_open_0"))).values_list(
            "symbol", flat=True
        )
        if recs:
            symbols = "\n".join(recs)
            TelegramAlert.send_message(symbols)

from datetime import datetime, time

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.smart_util import SmartInstrument, SmartTool
from core.tools import calculate_osc, get_macd_last_two_cross_over, get_param_config_tag


class MacdTrend(models.Model):
    date = models.DateField(verbose_name="Date")
    updated_date = models.DateField(verbose_name="Updated Date", null=True, blank=True)
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    price = models.FloatField(verbose_name="Price")
    percentage_change = models.FloatField(verbose_name="Percentage")
    ema_200 = models.FloatField(verbose_name="Ema200", null=True, blank=True)
    ema_50 = models.FloatField(verbose_name="Ema50", null=True, blank=True)
    last_close = models.FloatField(verbose_name="Last Close", null=True, blank=True)
    day_1_status = models.BooleanField(verbose_name="Day 1", default=False)
    day_2_status = models.BooleanField(verbose_name="Day 2", default=False)
    ema_200_percentage = models.FloatField(verbose_name="Ema 200 Percentage", default=0.0)
    trend_status = models.BooleanField(verbose_name="Trend Status", default=False)
    objects = models.Manager()

    class Meta:
        ordering = ["-date", "symbol"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_macd_trend")
        ]

    def get_date_difference(self):
        to_date = datetime.now()
        last_month_same_date = to_date - relativedelta(years=1, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_smart_token(self):
        try:
            obj = SmartInstrument(instrument=self.symbol)
            result = obj.get_instrument()
            self.smart_token = str(result.get("token"))
            self.save()
        except:
            pass

    def get_day_status(self):
        config = get_param_config_tag(tag="MYSURU")
        if self.price and self.ema_200 and (self.price < config["max_price"]) and (self.price > self.ema_200):
            self.trend_status = True
            self.save()

    def get_year_data(self):
        from_date, to_date = self.get_date_difference()
        tag_data = get_param_config_tag(tag="SMART_HISTORY")
        smart = SmartTool(**tag_data)
        smart.get_object()
        history_data = smart.get_historical_data(
            exchange="NSE",
            symboltoken=self.smart_token,
            interval="ONE_DAY",
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=to_date.strftime("%Y-%m-%d %H:%M"),
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)

        return df

    def generate_macd_osc(self):
        if not self.smart_token:
            return None

        df = self.get_year_data()
        data = get_macd_last_two_cross_over(df=df)
        print(data)

        self.ema_200 = round(data["ema_200"], 2)
        self.ema_50 = round(data["ema_50"], 2)
        self.updated_date = datetime.fromisoformat(data["date"])
        self.day_1_status = data["day_1_status"]
        self.day_2_status = data["day_2_status"]
        self.ema_200_percentage = round(data["ema_200_percentage"], 1)
        self.save()

        return True


class PriceAction(models.Model):
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    price_data = models.JSONField(verbose_name="Price Data", null=True, blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ["symbol"]
        constraints = [models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_price_action")]

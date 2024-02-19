from datetime import datetime, time

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db import models

from core.smart_util import SmartInstrument, SmartTool
from core.tools import get_stoch_crossover, get_macd_last_two_cross_over, get_param_config_tag, get_heikin_ashi


class StochHourlyTrend(models.Model):
    date = models.DateField(verbose_name="Date")
    updated_date = models.DateField(verbose_name="Updated Date", null=True, blank=True)
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier", null=True, blank=True)
    company_name = models.CharField(max_length=500, verbose_name="Company Name", null=True, blank=True)
    isin = models.CharField(max_length=100, verbose_name="Isin", null=True, blank=True)
    price = models.FloatField(verbose_name="Price", null=True, blank=True)
    percentage_change = models.FloatField(verbose_name="Percentage", null=True, blank=True)
    ema_200 = models.FloatField(verbose_name="Ema200", null=True, blank=True)
    ema_50 = models.FloatField(verbose_name="Ema50", null=True, blank=True)
    last_close = models.FloatField(verbose_name="Last Close", null=True, blank=True)
    stoch_status = models.BooleanField(verbose_name="Stoch Status", default=False)
    stoch_positive_trend = models.BooleanField(verbose_name="Stoch Positive Trend", default=False)
    ema_200_percentage = models.FloatField(verbose_name="Ema 200 Percentage", default=0.0)
    d_value = models.FloatField(verbose_name="D value", default=0.0)
    crossed = models.BooleanField(verbose_name="Stoch Crossed", default=False)
    trend_status = models.BooleanField(verbose_name="Trend Status", default=False)
    ha_positive = models.BooleanField(verbose_name="Heikin-Ashi Positive", default=False)
    ha_cross_yesterday = models.BooleanField(verbose_name="Heikin-Ashi Crossed Yesterday", default=False)
    ha_cross = models.BooleanField(verbose_name="Heikin-Ashi Crossed Yesterday", default=False)
    ha_wma_cross_yesterday = models.BooleanField(verbose_name="Heikin-Ashi WMA Crossed Yesterday", default=False)
    ha_wma_cross = models.BooleanField(verbose_name="Heikin-Ashi WMA Crossed", default=False)
    ha_wma_top = models.BooleanField(verbose_name="Heikin-Ashi WMA Top", default=False)
    objects = models.Manager()

    class Meta:
        ordering = ["-date", "symbol"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_stoch_trend")
        ]

    def get_date_difference(self):
        to_date = datetime.now()
        last_month_same_date = to_date - relativedelta(days=60)
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
            interval="ONE_HOUR",
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=to_date.strftime("%Y-%m-%d %H:%M"),
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def generate_stoch(self):
        if not self.smart_token:
            return None

        try:
            df = self.get_year_data()
            data = get_stoch_crossover(df=df)
            print(data)

            self.ema_200 = round(data["ema_200"], 2)
            self.ema_50 = round(data["ema_50"], 2)
            self.updated_date = data["date"]
            self.stoch_status = data["stoch_status"]
            self.stoch_positive_trend = data["stoch_positive_trend"]
            self.d_value = round(data["d_value"], 2)
            self.crossed = data["crossed"]
            self.ema_200_percentage = round(data["ema_200_percentage"], 1)
            self.price = data["last_price"]
            self.save()

            data = get_heikin_ashi(df=df)
            self.ha_positive = data["ha_positive"]
            self.ha_cross_yesterday = data["ha_cross_yesterday"]
            self.ha_cross = data["ha_cross"]
            self.ha_wma_cross_yesterday = data["ha_wma_cross_yesterday"]
            self.ha_wma_cross = data["ha_wma_cross"]
            self.ha_wma_top = data["ha_wma_top"]
            print(data)
            print(f"------------------{self.symbol}----------------------")
        except ValueError as ve:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(ve)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return True


class StochDailyTrend(models.Model):
    date = models.DateField(verbose_name="Date")
    updated_date = models.DateField(verbose_name="Updated Date", null=True, blank=True)
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier", null=True, blank=True)
    company_name = models.CharField(max_length=500, verbose_name="Company Name", null=True, blank=True)
    isin = models.CharField(max_length=100, verbose_name="Isin", null=True, blank=True)
    price = models.FloatField(verbose_name="Price", null=True, blank=True)
    percentage_change = models.FloatField(verbose_name="Percentage", null=True, blank=True)
    ema_200 = models.FloatField(verbose_name="Ema200", null=True, blank=True)
    ema_50 = models.FloatField(verbose_name="Ema50", null=True, blank=True)
    last_close = models.FloatField(verbose_name="Last Close", null=True, blank=True)
    stoch_status = models.BooleanField(verbose_name="Stoch Status", default=False)
    stoch_positive_trend = models.BooleanField(verbose_name="Stoch Positive Trend", default=False)
    ema_200_percentage = models.FloatField(verbose_name="Ema 200 Percentage", default=0.0)
    d_value = models.FloatField(verbose_name="D value", default=0.0)
    crossed = models.BooleanField(verbose_name="Stoch Crossed", default=False)
    trend_status = models.BooleanField(verbose_name="Trend Status", default=False)
    ha_positive = models.BooleanField(verbose_name="Heikin-Ashi Positive", default=False)
    ha_cross_yesterday = models.BooleanField(verbose_name="Heikin-Ashi Crossed Yesterday", default=False)
    ha_cross = models.BooleanField(verbose_name="Heikin-Ashi Crossed Yesterday", default=False)
    ha_wma_cross_yesterday = models.BooleanField(verbose_name="Heikin-Ashi WMA Crossed Yesterday", default=False)
    ha_wma_cross = models.BooleanField(verbose_name="Heikin-Ashi WMA Crossed", default=False)
    ha_wma_top = models.BooleanField(verbose_name="Heikin-Ashi WMA Top", default=False)
    objects = models.Manager()

    class Meta:
        ordering = ["-date", "symbol"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_stoch_trend")
        ]

    def get_date_difference(self):
        to_date = datetime.now() - relativedelta(days=1)
        if datetime.now().hour >= 13:
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
        df["date"] = pd.to_datetime(df["date"])
        return df

    def generate_stoch(self):
        if not self.smart_token:
            return None

        try:
            df = self.get_year_data()
            data = get_stoch_crossover(df=df)
            print(data)

            self.ema_200 = round(data["ema_200"], 2)
            self.ema_50 = round(data["ema_50"], 2)
            self.updated_date = data["date"]
            self.stoch_status = data["stoch_status"]
            self.stoch_positive_trend = data["stoch_positive_trend"]
            self.d_value = round(data["d_value"], 2)
            self.crossed = data["crossed"]
            self.ema_200_percentage = round(data["ema_200_percentage"], 1)
            self.price = data["last_price"]
            self.save()

            data = get_heikin_ashi(df=df)
            self.ha_positive = data["ha_positive"]
            self.ha_cross_yesterday = data["ha_cross_yesterday"]
            self.ha_cross = data["ha_cross"]
            self.ha_wma_cross_yesterday = data["ha_wma_cross_yesterday"]
            self.ha_wma_cross = data["ha_wma_cross"]
            self.ha_wma_top = data["ha_wma_top"]
            print(data)
            print(f"------------------{self.symbol}----------------------")
        except ValueError as ve:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(ve)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return True


class StochWeeklyTrend(models.Model):
    # Poll data
    date = models.DateField(verbose_name="Date")
    updated_date = models.DateField(verbose_name="Updated Date", null=True, blank=True)
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier", null=True, blank=True)
    company_name = models.CharField(max_length=500, verbose_name="Company Name", null=True, blank=True)
    isin = models.CharField(max_length=100, verbose_name="Isin", null=True, blank=True)
    price = models.FloatField(verbose_name="Price", null=True, blank=True)
    percentage_change = models.FloatField(verbose_name="Percentage", null=True, blank=True)

    # stoch calculated
    ema_200 = models.FloatField(verbose_name="Ema200", null=True, blank=True)
    ema_50 = models.FloatField(verbose_name="Ema50", null=True, blank=True)
    ema_200_percentage = models.FloatField(verbose_name="Ema 200 Percentage", default=0.0)
    d_value = models.FloatField(verbose_name="D value", default=0.0)

    stoch_status = models.BooleanField(verbose_name="Stoch Status", default=False)
    stoch_positive_trend = models.BooleanField(verbose_name="Stoch Positive Trend", default=False)
    crossed = models.BooleanField(verbose_name="Stoch Crossed", default=False)
    tend_to_positive = models.BooleanField(verbose_name="Tend to Positive", default=False)
    d_trend = models.BooleanField(verbose_name="D Trend", default=False)

    # conditional
    trend_status = models.BooleanField(verbose_name="Trend Status", default=False)

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "symbol"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_stoch_trend")
        ]

    def get_date_difference(self):
        to_date = datetime.now() - relativedelta(days=1)
        if datetime.now().hour >= 13:
            to_date = datetime.now()

        last_month_same_date = to_date - relativedelta(years=3, days=1)
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

        logic = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }

        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)
        dfw = df.resample("W").apply(logic)
        dfw.index = dfw.index - pd.tseries.frequencies.to_offset("6D")
        dfw.reset_index(inplace=True)
        return dfw

    def generate_stoch(self):
        if not self.smart_token:
            return None

        try:
            df = self.get_year_data()
            data = get_stoch_crossover(df=df)
            print(data)

            self.updated_date = data["date"]
            self.ema_200 = round(data["ema_200"], 2)
            self.ema_50 = round(data["ema_50"], 2)
            self.ema_200_percentage = round(data["ema_200_percentage"], 1)
            self.d_value = round(data["d_value"], 2)

            self.stoch_status = data["stoch_status"]
            self.crossed = data["crossed"]
            self.tend_to_positive = data["tend_to_positive"]
            self.d_trend = data["d_trend"]
            self.stoch_positive_trend = data["stoch_positive_trend"]
            self.price = data["last_price"]
            self.save()
            print(f"------------------{self.symbol}----------------------")
        except ValueError as ve:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(ve)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return True

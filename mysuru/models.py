from datetime import datetime, time

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db import models

from core.smart_util import SmartInstrument, SmartTool
from core.tools import (
    calculate_stochastic,
    get_param_config_tag,
    calculate_heikin_ashi,
    calculate_rsi,
    get_rsi,
    calculate_exponential_moving_average,
)


class Trend(models.Model):
    """Common Trend model"""
    created_date = models.DateField(verbose_name="Created Date", auto_now_add=True)
    updated_date = models.DateField(verbose_name="Updated Date", auto_now=True)

    symbol = models.CharField(max_length=50, verbose_name="Symbol")
    company_name = models.CharField(max_length=200, verbose_name="Company Name", null=True, blank=True)
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    smart_token_fetched = models.BooleanField(verbose_name="Smart Token Fetched", default=False)

    open = models.FloatField(verbose_name="Open", null=True, blank=True)
    high = models.FloatField(verbose_name="High", null=True, blank=True)
    low = models.FloatField(verbose_name="Low", null=True, blank=True)
    close = models.FloatField(verbose_name="Close", null=True, blank=True)
    volume = models.FloatField(verbose_name="Volume", null=True, blank=True)

    ema_20 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    ema_50 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    ema_200 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    ema_200_percentage = models.FloatField(verbose_name="EMA 200 Percentage", null=True, blank=True)

    stoch_black = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    stoch_red = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)

    stoch_black_previous = models.FloatField(verbose_name="Stoch Black Previous", null=True, blank=True)
    stoch_red_previous = models.FloatField(verbose_name="Stoch Red Previous", null=True, blank=True)

    ha_open = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    ha_high = models.FloatField(verbose_name="HA High", null=True, blank=True)
    ha_low = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    ha_close = models.FloatField(verbose_name="HA Close", null=True, blank=True)

    ha_open_previous = models.FloatField(verbose_name="HA Open Previous", null=True, blank=True)
    ha_high_previous = models.FloatField(verbose_name="HA High Previous", null=True, blank=True)
    ha_low_previous = models.FloatField(verbose_name="HA Low Previous", null=True, blank=True)
    ha_close_previous = models.FloatField(verbose_name="HA Close Previous", null=True, blank=True)

    rsi = models.FloatField(verbose_name="RSI", null=True, blank=True)
    rsi_previous = models.FloatField(verbose_name="RSI Previous", null=True, blank=True)

    is_fetched = models.BooleanField(verbose_name="Is Fetched", default=False)

    objects = models.Manager()

    class Meta:
        abstract = True
        ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def __str__(self):
        """String representation of trend"""
        return self.symbol

    def get_smart_token(self):
        """Get smart token from api"""
        try:
            obj = SmartInstrument(instrument=self.symbol)
            result = obj.get_instrument()
            self.smart_token = str(result.get("token"))
        except:
            pass

        self.smart_token_fetched = True
        self.save()

    def get_date_range(self):
        """Get date range for trend value"""
        raise NotImplementedError("Date range required for generating trend value.")

    def get_interval(self):
        """Get the interval for smart API"""
        raise NotImplementedError("Interval required for smart API.")

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        raise NotImplementedError("Reset date to weekly OHLC.")

    def get_smart_ohlc(self):
        """Get Open, High, Low, Close from smart API"""
        from_date, to_date = self.get_date_range()
        tag_data = get_param_config_tag(tag="SMART_HISTORY")
        smart = SmartTool(**tag_data)
        smart.get_object()
        history_data = smart.get_historical_data(
            exchange="NSE",
            symboltoken=self.smart_token,
            interval=self.get_interval(),
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=to_date.strftime("%Y-%m-%d %H:%M"),
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)
        df["date"] = pd.to_datetime(df["date"])
        return df

    def generate_trend_value(self):
        """Generate trend value"""
        if not self.smart_token:
            return None

        try:
            df = self.get_smart_ohlc()
            df = self.reset_date_ohlc(df=df)
            data = df.iloc[-1]
            self.open = round(data["open"], 2)
            self.high = round(data["high"], 2)
            self.low = round(data["low"], 2)
            self.close = round(data["close"], 2)
            self.volume = round(data["volume"], 2)

            data = calculate_exponential_moving_average(df=df)
            self.ema_200 = round(data["ema_200"], 2)
            self.ema_50 = round(data["ema_50"], 2)
            self.ema_20 = round(data["ema_20"], 2)
            self.ema_200_percentage = round(data["ema_200_percentage"], 2)

            data = calculate_stochastic(df=df)
            self.stoch_black = round(data["stoch_black"], 2)
            self.stoch_red = round(data["stoch_red"], 2)
            self.stoch_black_previous = round(data["stoch_black_previous"], 2)
            self.stoch_red_previous = round(data["stoch_red_previous"], 2)

            data = calculate_heikin_ashi(df=df)
            self.ha_open = round(data["ha_open"], 2)
            self.ha_high = round(data["ha_high"], 2)
            self.ha_low = round(data["ha_low"], 2)
            self.ha_close = round(data["ha_close"], 2)
            self.ha_open_previous = round(data["ha_open_previous"], 2)
            self.ha_high_previous = round(data["ha_high_previous"], 2)
            self.ha_low_previous = round(data["ha_low_previous"], 2)
            self.ha_close_previous = round(data["ha_close_previous"], 2)

            data = get_rsi(df=df)
            self.rsi = round(data["rsi"], 2)
            self.rsi_previous = round(data["rsi_previous"], 2)

            self.is_fetched = True
            self.save()
            print(f"------------------{self.symbol}----------------------")
        except ValueError as ve:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(ve)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return True


class HourlyTrend(Trend):
    """Hourly trend inherits from trend model"""

    class Meta:
        # ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def get_date_range(self):
        """Get date range for hourly trend"""
        to_date = datetime.now()
        last_month_same_date = to_date - relativedelta(days=60)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_interval(self):
        """Get the interval for smart API"""
        return "ONE_HOUR"

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        return df


class DailyTrend(Trend):
    """Daily trend inherits from trend model"""
    class Meta:
        # ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def get_date_range(self):
        """Get date range for daily trend"""
        to_date = datetime.now() - relativedelta(days=1)
        if datetime.now().hour >= 13:
            to_date = datetime.now()

        last_month_same_date = to_date - relativedelta(years=1, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_interval(self):
        """Get the interval for smart API"""
        return "ONE_DAY"

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
        return df


class WeeklyTrend(Trend):
    """Weekly trend inherits from trend model"""
    class Meta:
        # ordering = ["symbol"]
        constraints = [
            models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_trend")
        ]

    def get_date_range(self):
        """Get date range for weekly trend"""
        to_date = datetime.now() - relativedelta(days=1)
        if datetime.now().hour >= 13:
            to_date = datetime.now()

        last_month_same_date = to_date - relativedelta(years=3, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_interval(self):
        """Get the interval for smart API"""
        return "ONE_HOUR"

    def reset_date_ohlc(self, df):
        """Convert the daily data OHLC to weekly"""
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
    ha_cross_last_hour = models.BooleanField(verbose_name="Heikin-Ashi Crossed Last Hour", default=False)
    ha_cross = models.BooleanField(verbose_name="Heikin-Ashi Crossed Yesterday", default=False)
    ha_wma_cross_last_hour = models.BooleanField(verbose_name="Heikin-Ashi WMA Crossed Last Hour", default=False)
    ha_wma_cross = models.BooleanField(verbose_name="Heikin-Ashi WMA Crossed", default=False)
    ha_wma_top = models.BooleanField(verbose_name="Heikin-Ashi WMA Top", default=False)
    rsi = models.FloatField(verbose_name="D value", default=0.0)
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
            self.ha_cross_last_hour = data["ha_cross_yesterday"]
            self.ha_cross = data["ha_cross"]
            self.ha_wma_cross_last_hour = data["ha_wma_cross_yesterday"]
            self.ha_wma_cross = data["ha_wma_cross"]
            self.ha_wma_top = data["ha_wma_top"]

            data = get_rsi(df=df)
            self.rsi = data["rsi"]
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
    rsi = models.FloatField(verbose_name="D value", default=0.0)
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

            data = get_rsi(df=df)
            self.rsi = data["rsi"]
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

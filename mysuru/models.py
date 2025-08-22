from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db import models

from core.smart_util import SmartInstrument, SmartTool
from core.tools import (
    calculate_stochastic,
    get_param_config_tag,
    calculate_heikin_ashi,
    caculate_rsi,
    calculate_weighted_moving_average,
    get_ema,
    get_stochastic,
    get_heikin_ashi,
    get_rsi,
    get_ohlcv,
)


class TradingStatus(models.TextChoices):
    UP = "up", "UP"
    DOWN = "dn", "Down"


class StockData(models.Model):
    created_date = models.DateField(verbose_name="Created Date", auto_now_add=True)
    updated_date = models.DateField(verbose_name="Updated Date", auto_now=True)

    symbol = models.CharField(max_length=50, verbose_name="Symbol")
    company_name = models.CharField(max_length=200, verbose_name="Company Name", null=True, blank=True)
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    smart_token_fetched = models.BooleanField(verbose_name="Smart Token Fetched", default=False)

    is_wk_fetched = models.BooleanField(verbose_name="Week Fetched", default=False)
    wk_open = models.FloatField(verbose_name="Open", null=True, blank=True)
    wk_high = models.FloatField(verbose_name="High", null=True, blank=True)
    wk_low = models.FloatField(verbose_name="Low", null=True, blank=True)
    wk_close = models.FloatField(verbose_name="Close", null=True, blank=True)
    wk_close_0 = models.FloatField(verbose_name="Close", null=True, blank=True)
    wk_close_1 = models.FloatField(verbose_name="Close", null=True, blank=True)
    wk_close_2 = models.FloatField(verbose_name="Close", null=True, blank=True)
    wk_volume = models.FloatField(verbose_name="Volume", null=True, blank=True)
    wk_ema_5_0 = models.FloatField(verbose_name="EMA 5", null=True, blank=True)
    wk_ema_14_0 = models.FloatField(verbose_name="EMA 14", null=True, blank=True)
    wk_ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_ha_avg_0 = models.FloatField(verbose_name="HA Average", null=True, blank=True)
    wk_rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    wk_ema_5_1 = models.FloatField(verbose_name="EMA 5", null=True, blank=True)
    wk_ema_14_1 = models.FloatField(verbose_name="EMA 14", null=True, blank=True)
    wk_ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_ha_avg_1 = models.FloatField(verbose_name="HA Average", null=True, blank=True)
    wk_rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    wk_ema_5_2 = models.FloatField(verbose_name="EMA 5", null=True, blank=True)
    wk_ema_14_2 = models.FloatField(verbose_name="EMA 14", null=True, blank=True)
    wk_ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    wk_ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    wk_ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    wk_stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    wk_stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    wk_ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    wk_ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    wk_ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    wk_ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    wk_ha_avg_2 = models.FloatField(verbose_name="HA Average", null=True, blank=True)
    wk_rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    is_day_fetched = models.BooleanField(verbose_name="Day Fetched", default=False)
    day_open = models.FloatField(verbose_name="Open", null=True, blank=True)
    day_high = models.FloatField(verbose_name="High", null=True, blank=True)
    day_low = models.FloatField(verbose_name="Low", null=True, blank=True)
    day_close = models.FloatField(verbose_name="Close", null=True, blank=True)
    day_close_0 = models.FloatField(verbose_name="Close", null=True, blank=True)
    day_close_1 = models.FloatField(verbose_name="Close", null=True, blank=True)
    day_close_2 = models.FloatField(verbose_name="Close", null=True, blank=True)
    day_volume = models.FloatField(verbose_name="Volume", null=True, blank=True)
    day_ema_5_0 = models.FloatField(verbose_name="EMA 5", null=True, blank=True)
    day_ema_14_0 = models.FloatField(verbose_name="EMA 14", null=True, blank=True)
    day_ema_20_0 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_0 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_0 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_0 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_0 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_0 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_0 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_0 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_0 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_ha_avg_0 = models.FloatField(verbose_name="HA Average", null=True, blank=True)
    day_rsi_0 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    day_ema_5_1 = models.FloatField(verbose_name="EMA 5", null=True, blank=True)
    day_ema_14_1 = models.FloatField(verbose_name="EMA 14", null=True, blank=True)
    day_ema_20_1 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_1 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_1 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_1 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_1 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_1 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_1 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_1 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_1 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_ha_avg_1 = models.FloatField(verbose_name="HA Average", null=True, blank=True)
    day_rsi_1 = models.FloatField(verbose_name="RSI", null=True, blank=True)
    day_ema_5_2 = models.FloatField(verbose_name="EMA 5", null=True, blank=True)
    day_ema_14_2 = models.FloatField(verbose_name="EMA 14", null=True, blank=True)
    day_ema_20_2 = models.FloatField(verbose_name="EMA 20", null=True, blank=True)
    day_ema_50_2 = models.FloatField(verbose_name="EMA 50", null=True, blank=True)
    day_ema_200_2 = models.FloatField(verbose_name="EMA 200", null=True, blank=True)
    day_stoch_black_2 = models.FloatField(verbose_name="Stoch Black", null=True, blank=True)
    day_stoch_red_2 = models.FloatField(verbose_name="Stoch Red", null=True, blank=True)
    day_ha_open_2 = models.FloatField(verbose_name="HA Open", null=True, blank=True)
    day_ha_high_2 = models.FloatField(verbose_name="HA High", null=True, blank=True)
    day_ha_low_2 = models.FloatField(verbose_name="HA Low", null=True, blank=True)
    day_ha_close_2 = models.FloatField(verbose_name="HA Close", null=True, blank=True)
    day_ha_avg_2 = models.FloatField(verbose_name="HA Average", null=True, blank=True)
    day_rsi_2 = models.FloatField(verbose_name="RSI", null=True, blank=True)

    trading_updated_at = models.DateTimeField(verbose_name="Trading Updated at", null=True, blank=True)
    is_trading = models.BooleanField(verbose_name="Is Trading", default=False)
    trading_status = models.CharField(max_length=2, choices=TradingStatus.choices, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ["symbol"]
        constraints = [models.UniqueConstraint(fields=["symbol"], name="%(app_label)s_%(class)s_unique_stock")]

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

    def get_smart_ohlc(self, interval, days):
        """Get Open, High, Low, Close from smart API"""
        from_date = datetime.now() - relativedelta(days=days)
        tag_data = get_param_config_tag(tag="SMART_HISTORY")
        smart = SmartTool(**tag_data)
        smart.get_object()
        history_data = smart.get_historical_data(
            exchange="NSE",
            symboltoken=self.smart_token,
            interval=interval,
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=datetime.now().strftime("%Y-%m-%d %H:%M"),
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)
        df["date"] = pd.to_datetime(df["date"])

        return df

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

    def get_fetch_params(self, data_type):
        params = {
            "wk": ("ONE_DAY", 900),
            "day": ("ONE_DAY", 400),
        }
        return params.get(data_type)

    def generate_trend_value(self, data_type, df=None):
        """Generate trend value"""
        if not self.smart_token:
            return None

        try:
            interval, days = self.get_fetch_params(data_type)
            if df is None:
                df = self.get_smart_ohlc(interval=interval, days=days)
            if data_type == "wk":
                self.generate_trend_value("day", df=df)
                df = self.reset_date_ohlc(df=df)

            df_ohlcv = get_ohlcv(df=df, data_type=data_type)
            df_ha = calculate_heikin_ashi(df=df)
            df_ema = calculate_weighted_moving_average(df=df_ha)
            df_stoch = calculate_stochastic(df=df_ha)
            df_rsi = caculate_rsi(df=df_ha)

            data_ema = get_ema(df_ema, data_type)
            data_stoch = get_stochastic(df_stoch, data_type)
            data_ha = get_heikin_ashi(df_ha, data_type)
            data_rsi = get_rsi(df_rsi, data_type)

            all_data = df_ohlcv | data_ema | data_stoch | data_ha | data_rsi
            for attr, value in all_data.items():
                setattr(self, attr, value)

            setattr(self, f"is_{data_type}_fetched", True)
            self.save()
            print(f"------------------{self.symbol}----{data_type}------------------")
        except ValueError as ve:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(ve)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        except AttributeError as ae:
            print(ae)

        return True

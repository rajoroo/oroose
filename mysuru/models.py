from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from core.smart_util import SmartInstrument, SmartTool
from core.tools import calculate_macd, get_param_config_tag, calculate_osc
import pandas as pd


class DayStatus(models.TextChoices):
    YES = "YES", _("Yes")
    NO = "NO", _("No")


class TrendStatus(models.TextChoices):
    TO_BUY = "TO_BUY", "To Buy"
    PURCHASED = "PURCHASED", "Purchased"
    TO_SELL = "TO_SELL", "To Sell"
    SOLD = "SOLD", "Sold"


class PlStatus(models.TextChoices):
    WINNER = "WR", _("Winner")
    RUNNER = "RR", _("Runner")
    INPROG = "IP", _("In-Progress")


class TopTen(models.Model):
    date = models.DateField(verbose_name="Date")
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    ksec_token = models.CharField(max_length=50, verbose_name="Ksec Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    percentage_change = models.FloatField(verbose_name="Percentage")
    is_accepted = models.BooleanField(default=False, verbose_name="Is Accepted")
    ema_200 = models.FloatField(verbose_name="Ema200", null=True, blank=True)
    ema_50 = models.FloatField(verbose_name="Ema50", null=True, blank=True)
    last_close = models.FloatField(verbose_name="Last Close", null=True, blank=True)
    yesterday_macd = models.FloatField(verbose_name="Yesterday MACD", null=True, blank=True)
    yesterday_macd_signal = models.FloatField(verbose_name="Yesterday MACD Signal", null=True, blank=True)
    yesterday_macd_histogram = models.FloatField(verbose_name="Yesterday MACD Histogram", null=True, blank=True)
    today_macd = models.FloatField(verbose_name="MACD", null=True, blank=True)
    today_macd_signal = models.FloatField(verbose_name="MACD Signal", null=True, blank=True)
    today_macd_histogram = models.FloatField(verbose_name="MACD Histogram", null=True, blank=True)
    macd_status = models.CharField(
        max_length=5,
        choices=DayStatus.choices,
        default=DayStatus.NO,
    )
    yesterday_osc = models.FloatField(verbose_name="Yesterday OSC", null=True, blank=True)
    yesterday_osc_signal = models.FloatField(verbose_name="Yesterday OSC Signal", null=True, blank=True)
    today_osc = models.FloatField(verbose_name="OSC", null=True, blank=True)
    today_osc_signal = models.FloatField(verbose_name="OSC Signal", null=True, blank=True)
    osc_status = models.CharField(
        max_length=5,
        choices=DayStatus.choices,
        default=DayStatus.NO,
    )
    day_status = models.CharField(
        max_length=5,
        choices=DayStatus.choices,
        default=DayStatus.NO,
    )
    objects = models.Manager()

    class Meta:
        ordering = ["-date", "symbol"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_top_ten")
        ]

    def get_date_difference(self):
        now = datetime.now()
        if now.hour < 18:
            now = datetime.now() - relativedelta(days=1)

        to_date = now
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
        if (
                self.last_price
                and self.ema_200
                and self.ema_50
                and self.today_osc
                and self.today_osc_signal
                and self.yesterday_osc
                and self.yesterday_osc_signal
                and self.yesterday_macd_signal
                and self.yesterday_macd
                and self.today_macd_signal
                and self.today_macd
                and (self.last_price > config["min_price"])
                and (self.last_price < config["max_price"])
                and (self.last_price > self.ema_200)
                and (self.ema_50 > self.ema_200)
                and (self.yesterday_osc_signal > self.yesterday_osc)
                and (self.today_osc > self.today_osc_signal)
                and (self.yesterday_macd_signal > self.yesterday_macd)
                and (self.today_macd_signal > self.today_macd)
        ):
            self.day_status = DayStatus.YES
        else:
            self.day_status = DayStatus.NO

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
            todate=to_date.strftime("%Y-%m-%d %H:%M")
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)

        return df

    def generate_macd_osc(self):
        df = self.get_year_data()
        df = calculate_osc(df=df)
        result_df = calculate_macd(df=df)

        df['ema_200'] = df['close'].rolling(window=200).mean()
        df['ema_50'] = df['close'].rolling(window=50).mean()
        self.ema_200 = round(df["ema_200"].iloc[-1], 2)
        self.ema_50 = round(df["ema_50"].iloc[-1], 2)

        if df.shape[0] > 16:
            self.yesterday_osc = round(df['d'].iloc[-2], 2)
            self.yesterday_osc_signal = round(df['k_smooth'].iloc[-2], 2)
            self.today_osc = round(df['d'].iloc[-1], 2)
            self.today_osc_signal = round(df['k_smooth'].iloc[-1], 2)

            self.yesterday_macd = round(result_df['macd'].iloc[-2], 2)
            self.yesterday_macd_signal = round(result_df['macd_s'].iloc[-2], 2)
            self.yesterday_macd_histogram = round(result_df['macd_h'].iloc[-2], 2)

            self.today_macd = round(result_df['macd'].iloc[-1], 2)
            self.today_macd_signal = round(result_df['macd_s'].iloc[-1], 2)
            self.today_macd_histogram = round(result_df['macd_h'].iloc[-1], 2)

            if self.yesterday_osc_signal > self.yesterday_osc and self.today_osc > self.today_osc_signal:
                self.osc_status = DayStatus.YES

            if self.yesterday_macd_signal > self.yesterday_macd and self.today_macd > self.today_macd_signal:
                self.macd_status = DayStatus.YES

            self.save()

        return True

from datetime import datetime, timedelta, time

import numpy as np
from django.db import models
import pandas as pd
from core.choice import PlStatus,FhZeroStatus
from core.tools import calculate_rsi, get_param_config_tag, get_today_datetime
from core.smart_util import SmartInstrument, SmartTool
from core.ks_util import KsecInstrument
from dateutil.relativedelta import relativedelta
from stockwatch.stocks import PriceBand


from stockwatch.choice import SignalStatus


class StockWatchFh(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    stock_data = models.JSONField(verbose_name="Stock Data", null=True, blank=True)
    objects = models.Manager()


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    rank = models.IntegerField(verbose_name="Rank")
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    smart_token = models.CharField(max_length=50, verbose_name="Smart Token", null=True, blank=True)
    ksec_token = models.CharField(max_length=50, verbose_name="Ksec Token", null=True, blank=True)
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    open_price = models.FloatField(verbose_name="Open Price", null=True, blank=True)
    percentage_change = models.FloatField(verbose_name="Percentage")
    signal_status = models.CharField(
        max_length=5,
        choices=SignalStatus.choices,
        default=SignalStatus.INPROG,
    )
    is_valid = models.BooleanField(default=False, verbose_name="Is Valid")
    pp2 = models.FloatField(verbose_name="PP2", null=True, blank=True)
    pp1 = models.FloatField(verbose_name="PP1", null=True, blank=True)
    pp = models.FloatField(verbose_name="PP0", null=True, blank=True)
    pp_price = models.FloatField(verbose_name="PP0 Price", null=True, blank=True)
    pp1_price = models.FloatField(verbose_name="PP1 Price", null=True, blank=True)
    pp2_price = models.FloatField(verbose_name="PP2 Price", null=True, blank=True)

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "rank"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_five_hundred")
        ]

    def get_date_difference(self):
        to_date = datetime.now()
        last_month_same_date = to_date - relativedelta(months=1, days=1)
        exact_time = time(hour=9, minute=15)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_smart_token(self):
        obj = SmartInstrument(instrument=self.symbol)
        result = obj.get_instrument()
        self.smart_token = str(result.get("token"))
        self.save()

    def get_ksec_token(self):
        obj = KsecInstrument(instrument=self.symbol)
        result = obj.get_instrument()
        self.ksec_token = str(result.get("pSymbol"))
        self.save()

    def is_valid_stock(self):
        band = PriceBand(instrument=self.symbol)
        self.is_valid = band.get_valid_instrument()
        self.save()

    def get_signal_status(self):
        from_date, to_date = self.get_date_difference()

        if not self.smart_token:
            return True

        if self.rank > 9 and (not self.fhzerouptrend_set.filter(pl_status=PlStatus.INPROG).exists()):
            return True

        tag_data = get_param_config_tag(tag="SMART_TRADE")
        smart = SmartTool(**tag_data)
        smart.get_object()
        history_data = smart.get_historical_data(
            exchange="NSE",
            symboltoken=self.smart_token,
            interval="FIVE_MINUTE",
            fromdate=from_date.strftime("%Y-%m-%d %H:%M"),
            todate=to_date.strftime("%Y-%m-%d %H:%M")
        )

        df = pd.DataFrame(history_data)
        df[["date", "open", "high", "low", "close", "volume"]] = pd.DataFrame(df.data.tolist(), index=df.index)

        current_list = df["close"].to_list()

        if current_list and len(current_list) > 16:
            df = pd.DataFrame({'close': current_list})
            result_df = calculate_rsi(df=df)

            result_2 = round(result_df['rsi'].iloc[-3], 2)
            result_1 = round(result_df['rsi'].iloc[-2], 2)
            result = round(result_df['rsi'].iloc[-1], 2)

            print(result_2, result_1, result, self.symbol)
            self.pp2 = result_2
            self.pp1 = result_1
            self.pp = result
            self.pp2_price = current_list[-3]
            self.pp1_price = current_list[-2]
            self.pp_price = current_list[-1]
            self.save()
        return True

    def get_basic_requirement(self):
        requirement = False

        config = get_param_config_tag(tag="BENGALURU")
        start_time = get_today_datetime(time_str=config.get("start_time"))
        end_time = get_today_datetime(time_str=config.get("end_time"))
        fhz_status = [FhZeroStatus.TO_BUY, FhZeroStatus.PURCHASED, FhZeroStatus.TO_SELL]
        pl_status = [PlStatus.WINNER, PlStatus.INPROG]

        if (
            config.get("bengaluru_status")
            and self.is_valid is True
            and (self.rank <= 9)
            and (config["min_price"] <= self.last_price <= config["max_price"])
            and (self.percentage_change <= config["max_percentage"])
            and (self.fhzerouptrend_set.all().count() < config["max_buy_order"])
            and (not self.fhzerouptrend_set.filter(status__in=fhz_status).exists())
            and (not self.fhzerouptrend_set.filter(pl_status__in=pl_status).exists())
            and (not self.fhzerouptrend_set.filter(error=True).exists())
            and (start_time <= datetime.now() <= end_time)
            and (datetime.today().weekday() < 5)
            and self.pp
            and self.pp1
            and self.pp2
            and self.pp_price
            and self.pp1_price
            and self.pp2_price
        ):
            requirement = True

        return requirement

    def get_pre_order_requirement(self):
        requirement = True
        before_20_min = datetime.now() - timedelta(minutes=20)

        if self.fhzerouptrend_set.all():
            latest_fhz = self.fhzerouptrend_set.latest("updated_date")
            if latest_fhz.updated_date > before_20_min:
                requirement = False

        return requirement

    def get_standard_requirement(self):
        requirement = False

        # Return False is the condition didn't pass basic and pre-order requirement
        if not (self.get_basic_requirement() and self.get_pre_order_requirement()):
            return False

        if (
            (self.pp > self.pp1 > 65 > self.pp2)
            or (
                (self.rank <= 5)
                and (self.pp_price > self.pp1_price > self.pp2_price)
                and (60 < self.pp < 80)
            )
        ):
            requirement = True

        return requirement

from datetime import datetime, timedelta, time

import numpy as np
from django.db import models
import pandas as pd
from core.zero_util import get_history_five_min, get_kite, get_history_day
from core.choice import FhZeroStatus, PlStatus
from core.tools import calculate_rsi, get_param_config_tag
from core.smart_util import SmartInstrument, SmartTool
from dateutil.relativedelta import relativedelta


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
    token = models.CharField(max_length=50, verbose_name="Token", null=True, blank=True)
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

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "rank"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_five_hundred")
        ]

    def get_date_diffetence(self):
        to_date = datetime.today()
        last_month_same_date = to_date - relativedelta(months=1, days=1)
        exact_time = time(hour=9, minute=10)
        from_date = datetime.combine(last_month_same_date, exact_time)
        return from_date, to_date

    def get_smart_token(self):
        obj = SmartInstrument(instrument=self.symbol)
        result = obj.get_instrument()
        self.token = result.get("token")
        self.save()

    def is_valid_stock(self):
        result = False

        config = get_param_config_tag(tag="SMART")
        obj = SmartTool(
            api_key=config["api_key"],
            client_code=config["client_code"],
            password=config["password"],
            totp=config["totp"],
            jwt_token=config["jwt_token"],
            refresh_token=config["refresh_token"],
            feed_token=config["feed_token"],
        )
        obj.get_object()
        data = obj.get_ltp_data("NSE", self.symbol, self.token)
        print(data)

        #
        #
        #
        #
        # kite = get_kite()
        #
        # instrument = f"NSE:{symbol}"
        # quote_response = kite.quote(instrument)
        #
        # lower_circuit = quote_response[instrument]["lower_circuit_limit"]
        # upper_circuit = quote_response[instrument]["upper_circuit_limit"]
        #
        # last_price = quote_response[instrument]["ohlc"]["close"]
        # price_lower = last_price - (last_price * 0.09)
        # price_upper = last_price + (last_price * 0.09)
        #
        # if lower_circuit < price_lower < price_upper < upper_circuit:
        #     result = True
        #
        # self.is_valid = result
        # self.save()

    def get_signal_status(self, time_obj):
        signal_status = SignalStatus.INPROG
        today = datetime.today() - timedelta(days=31)
        exact_time = time(hour=9, minute=10)
        from_date = datetime.combine(today, exact_time)

        # if not (
        #         (self.fhzerodowntrend_set.filter(pl_status=PlStatus.INPROG).exists()
        #             or self.rank <= 9)
        #         or (self.fhzerouptrend_set.filter(pl_status=PlStatus.INPROG).exists()
        #              or self.rank <= 9)
        # ):
        #     return signal_status

        current_list = get_history_five_min(token=self.token, open_price=self.open_price, from_date=from_date, to_date=time_obj)

        if current_list and len(current_list) > 16:
            df = pd.DataFrame({'close': current_list})
            result_df = calculate_rsi(df=df)

            result_2 = result_df['rsi'].iloc[-3]
            result_1 = result_df['rsi'].iloc[-2]
            result = result_df['rsi'].iloc[-1]

            print(result_2, result_1, result, self.symbol)
            self.pp2 = result_2
            self.pp1 = result_1
            self.pp = result
            self.save()
        return signal_status

from datetime import datetime, timedelta, time

import numpy as np
from django.db import models
import pandas as pd
from core.zero_util import get_history_five_min, get_kite, get_history_day
from core.choice import FhZeroStatus, PlStatus
from core.tools import calculate_rsi, get_param_config_tag
from core.smart_util import SmartInstrument, SmartTool
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

    def get_date_difference(self):
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
        band = PriceBand(instrument=self.symbol)
        self.is_valid = band.get_valid_instrument()
        self.save()

    def get_signal_status(self, time_obj):
        signal_status = SignalStatus.INPROG
        from_date, to_date = self.get_date_difference()

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

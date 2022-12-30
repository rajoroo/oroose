from datetime import timedelta

import numpy as np
from django.db import models
import pandas as pd

from stockwatch.choice import SignalStatus


class StockWatchFh(models.Model):
    date = models.DateField(verbose_name="Date")
    created_date = models.DateTimeField(verbose_name="Created Date")
    stock_data = models.JSONField(verbose_name="Stock Data", null=True, blank=True)
    objects = models.Manager()


class FiveHundred(models.Model):
    date = models.DateField(verbose_name="Date")
    time = models.DateTimeField(verbose_name="Time")
    created_date = models.DateTimeField(verbose_name="Created Date")
    rank = models.IntegerField(verbose_name="Rank")
    highest_rank = models.IntegerField(verbose_name="Highest Rank", null=True, blank=True)
    lowest_rank = models.IntegerField(verbose_name="Lowest Rank", null=True, blank=True)
    previous_rank = models.IntegerField(verbose_name="Previous Rank", null=True, blank=True)
    symbol = models.CharField(max_length=200, verbose_name="Symbol")
    identifier = models.CharField(max_length=200, verbose_name="Identifier")
    company_name = models.CharField(max_length=500, verbose_name="Company Name")
    isin = models.CharField(max_length=100, verbose_name="Isin")
    last_price = models.FloatField(verbose_name="Price")
    previous_price = models.FloatField(verbose_name="Previous Price")
    previous_price_20min = models.FloatField(verbose_name="Previous Price 20min", default=0.0)
    percentage_change = models.FloatField(verbose_name="Percentage")
    signal_status = models.CharField(
        max_length=5,
        choices=SignalStatus.choices,
        default=SignalStatus.INPROG,
    )

    objects = models.Manager()

    class Meta:
        ordering = ["-date", "rank"]
        constraints = [
            models.UniqueConstraint(fields=["date", "symbol"], name="%(app_label)s_%(class)s_unique_five_hundred")
        ]

    def get_previous_20_min(self, time_obj):
        stock_watch = 0.0
        before_20_min = time_obj - timedelta(minutes=20)
        before_30_min = time_obj - timedelta(minutes=30)
        obj = StockWatchFh.objects.filter(created_date__range=(before_30_min, before_20_min)).order_by("-id").first()

        if (not obj) and (not hasattr(obj, "stock_data")):
            return stock_watch

        stock_watch = obj.stock_data.get(self.symbol)

        if stock_watch:
            return stock_watch["last_price"]
        return 0.0

    def get_signal_status(self, time_obj, price):
        signal_status = SignalStatus.INPROG
        before_20_intervals = time_obj - timedelta(hours=1, minutes=40)
        obj = StockWatchFh.objects.filter(created_date__range=(before_20_intervals, time_obj)).order_by("-id")

        if (not obj) or (obj.count() < 18):
            return signal_status

        print(self.symbol)
        data = []
        for rec in obj:
            # print(rec.stock_data)
            if hasattr(rec, "stock_data"):
                if rec.stock_data.get(self.symbol):
                    data.append(rec.stock_data.get(self.symbol)["last_price"])

        result = np.mean(data)

        signal_status = SignalStatus.BUY if price > result else SignalStatus.SELL
        return signal_status

    def get_rsi_status(self, time_obj):
        signal_status = SignalStatus.INPROG
        before_20_intervals = time_obj - timedelta(hours=1, minutes=40)
        obj = StockWatchFh.objects.filter(created_date__range=(before_20_intervals, time_obj)).order_by("-id")

        if (not obj) or (obj.count() < 16):
            return signal_status
        # print(obj.values("id", "created_date"))
        data = []
        for rec in obj:
            if hasattr(rec, "stock_data"):
                if rec.stock_data.get(self.symbol):
                    data.append(rec.stock_data.get(self.symbol)["last_price"])

        current_list = data[0:15]
        previous_list = data[1:16]

        current_list.reverse()
        previous_list.reverse()
        # print(current_list)
        # print(previous_list)

        df_current = pd.DataFrame({'close': current_list})
        df_previous = pd.DataFrame({'close': previous_list})
        # print(df_current, df_previous)
        result = self.calculate_rsi(df_current)
        pre_result = self.calculate_rsi(df_previous)

        if result < 70 < pre_result:
            signal_status = SignalStatus.SELL
        elif result > 70 > pre_result:
            signal_status = SignalStatus.BUY
        print(result, pre_result, signal_status, self.symbol)
        return signal_status

    def calculate_rsi(self, df):
        df['change'] = df['close'].diff(1)  # Calculate change

        # calculate gain / loss from every change
        df['gain'] = np.select([df['change'] > 0, df['change'].isna()],
                               [df['change'], np.nan],
                               default=0)
        df['loss'] = np.select([df['change'] < 0, df['change'].isna()],
                               [-df['change'], np.nan],
                               default=0)

        # create avg_gain /  avg_loss columns with all nan
        df['avg_gain'] = np.nan
        df['avg_loss'] = np.nan

        n = 14  # what is the window

        # keep first occurrence of rolling mean
        # df['avg_gain'][n] = df['gain'].rolling(window=n).mean().dropna().iloc[0]
        # df['avg_loss'][n] = df['loss'].rolling(window=n).mean().dropna().iloc[0]
        # Alternatively
        df['avg_gain'][n] = df.loc[:n, 'gain'].mean()
        df['avg_loss'][n] = df.loc[:n, 'loss'].mean()

        # This is not a pandas way, looping through the pandas series, but it does what you need
        for i in range(n + 1, df.shape[0]):
            df['avg_gain'].iloc[i] = (df['avg_gain'].iloc[i - 1] * (n - 1) + df['gain'].iloc[i]) / n
            df['avg_loss'].iloc[i] = (df['avg_loss'].iloc[i - 1] * (n - 1) + df['loss'].iloc[i]) / n

        # calculate rs and rsi
        df['rs'] = df['avg_gain'] / df['avg_loss']
        df['rsi'] = 100 - (100 / (1 + df['rs']))

        return df['rsi'].iloc[-1]
